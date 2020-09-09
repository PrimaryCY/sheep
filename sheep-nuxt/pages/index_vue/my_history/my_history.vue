<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <div class="wrap">
        <div class="detail-body">
            <div class="header">
                <page-heaeder
                        text="我的浏览">
                </page-heaeder>
            </div>
            <el-divider>
            </el-divider>
            <div id="l" class="content">
                <el-form label-position="left" ref="filter_collect">
                    <el-row type="flex" :gutter="20">
                        <el-col :span="16">
                            <el-form-item
                                    label-width="60px"
                                    label="关键字:">
                                <el-input placeholder="文章/问题名称"
                                          clearable
                                          size="small"
                                          maxlength="100"
                                          show-word-limit
                                          v-model="form.search"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item
                                    label-width="45px"
                                    label="类别:">
                                <el-cascader
                                        ref="cascader"
                                        clearable
                                        size="small"
                                        :options="option.post_category"
                                        v-model="form.post_category"
                                        :props="{value:'id',label:'name',children:'child'}"
                                        :show-all-levels="false">
                                    <template slot-scope="{ node, data }">
                                        <span>{{ data.name }}</span>
                                        <span v-if="!node.isLeaf"> ({{ data.child.length }}) </span>
                                    </template>
                                </el-cascader>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row type="flex" :gutter="20">
                        <el-col :span="12">
                            <el-form-item
                                    label-width="75px"
                                    label="浏览日期:">
                                <el-date-picker
                                        v-model="form.time_range"
                                        type="datetimerange"
                                        align="right"
                                        unlink-panels
                                        format="yyyy-MM-dd hh:mm"
                                        value-format="yyyy-MM-dd-hh:mm"
                                        range-separator="至"
                                        start-placeholder="开始日期"
                                        end-placeholder="结束日期"
                                        size="small"
                                        :picker-options="pickerOptions">
                                </el-date-picker>
                            </el-form-item>
                        </el-col>
                        <el-col :span="7">
                            <el-form-item
                                    label-width="75px"
                                    label="类型:">
                                <el-select	v-model="form.post_type"
                                              clearable
                                              size="small"
                                              placeholder="请选择">
                                    <el-option
                                            label="文章"
                                            value="1"
                                    ></el-option>
                                    <el-option
                                            label="提问"
                                            value="2"
                                    ></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="5">
                            <el-form-item>
                                <el-button type="primary" @click="filter_collect" size="small">查询</el-button>
                                <el-button type="danger" @click="form={}" size="small">重置</el-button>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
                <list
                        :need_border_top="false"
                        :list="data.results">
                    <template v-slot:item-content="data">
                        <history_post_item
                                :post="data.item">
                        </history_post_item>
                    </template>
                </list>
                <div class="collect-pagination">
                    <pagination
                            @change="_get_history_data"
                            :pagination_config="{layout:'total, sizes, prev, pager, next',background:true}"
                            :params="params"
                            :pager="data"></pagination>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState} from 'vuex'

    import {
        api_user_history
    } from '../../../api'
    import list from '@/components/list/list'
    import history_post_item from "../../../components/list/item/history_post_item"
    import pageHeaeder from "../../../components/common/pageHeaeder"
    import {pickerOptions} from '../../../utils/util'
    import pagination from '../../../components/pagination'


    export default {
        name: 'my_history',
        data() {
            return {
                pickerOptions,
                not_found: false,
                collect_desc: {
                    name: '读取中...',
                    desc: '数据正在快马加鞭的赶过来!'
                },
                data: {},
                params: {
                    limit: 10,
                    offset: 0,
                    collect_id: this.$route.params.id,
                },
                form: {
                    name: null,
                    ordering: null,
                    post_type: null,
                }
            }
        },
        methods: {
            async _get_history_data() {
                // 获取用户历史浏览记录
                this.move_to_top()
                let loading = this.openLoading({
                    text: '加载中...',
                    target: '#l'
                })
                let res = await api_user_history.list(this.params)
                res = res.data
                if (res.code !== 2000) {
                    loading.close()
                    return this.$message(res.msg)
                }
                this.data = res.data
                loading.close()
            },
            filter_collect() {
                // 点击查询
                if (this.form.time_range) {
                    this.params.start_time = this.form.time_range[0]
                    this.params.end_time = this.form.time_range[1]
                } else {
                    this.params.start_time = null
                    this.params.end_time = null
                }
                if (this.form.post_category) {
                    this.params.category = this.form.post_category[this.form.post_category.length - 1]
                } else {
                    this.params.category = null
                }
                this.params.search = this.form.search
                this.params.post_type = this.form.post_type
                this._get_history_data()
            }
        },
        created() {
            if (process.server) return
            this._get_history_data()
        },
        computed: {
            ...mapState(['option'])
        },
        inject: ['push', 'move_to_top'],
        components: {
            list,
            pagination,
            pageHeaeder,
            history_post_item
        }
    }
</script>

<style scoped lang="scss">

    .wrap {

        .detail-body {
            width: 100%;
        }
        .collect-image {
            width: 50px;
            height: 50px;
            border-radius: 5px;
            object-fit: cover;
            cursor: pointer;
        }

        .content {
            min-height: 40vh;

            .collect-pagination {
                padding: 8%;
                text-align: center;
            }
        }
    }
</style>
