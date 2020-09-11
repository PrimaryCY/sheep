<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <div class="my_post">
        <div class="header-filter">
            <el-form label-position="left">
                <el-row type="flex" :gutter="20">
                    <el-col :span="16">
                        <el-form-item
                                label-width="60px"
                                label="关键字:">
                            <el-input placeholder="文章名称"
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
                                label="创建日期:">
                            <el-date-picker
                                    v-model="form.created_time_range"
                                    type="daterange"
                                    align="right"
                                    unlink-panels
                                    range-separator="至"
                                    start-placeholder="开始日期"
                                    value-format="yyyy-MM-dd"
                                    end-placeholder="结束日期"
                                    size="small"
                                    :picker-options="pickerOptions">
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col :span="7">
                        <el-form-item
                                label-width="75px"
                                label="排序方式:">
                            <el-select v-model="form.ordering"
                                       clearable
                                       size="small"
                                       placeholder="请选择">
                                <el-option
                                        label="点赞(正排序)"
                                        value="praise_num"
                                ></el-option>
                                <el-option
                                        label="点赞(倒排序)"
                                        value="-praise_num"
                                ></el-option>
                                <el-option
                                        label="阅读(正排序)"
                                        value="read_num"
                                ></el-option>
                                <el-option
                                        label="阅读(倒排序)"
                                        value="-read_num"
                                ></el-option>
                                <el-option
                                        label="收藏(正排序)"
                                        value="like_num"
                                ></el-option>
                                <el-option
                                        label="收藏(倒排序)"
                                        value="-like_num"
                                ></el-option>
                                <el-option
                                        label="评论(正排序)"
                                        value="post_num"
                                ></el-option>
                                <el-option
                                        label="评论(倒排序)"
                                        value="-post_num"
                                ></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="5">
                        <el-form-item>
                            <el-button type="primary" @click="filter_post" size="small">查询</el-button>
                            <el-button type="danger" @click="form={}" size="small">重置</el-button>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
        </div>
        <list :list="posts.results">
            <template v-slot:item-content="data">
                <user_post_item
                        :post="data.item"
                        @update_func="update_post"
                        @delete_func="delete_post"
                        :editor="true">
                </user_post_item>
            </template>
        </list>
        <div class="footer-pagination">
            <pagination
                    @change="_get_user_posts"
                    :pagination_config="{layout:'total, sizes, prev, pager, next',background:true}"
                    :params="params"
                    :pager="posts"></pagination>
        </div>

    </div>
</template>

<script>
    import {mapState} from 'vuex'

    import {api_user_post} from "@/api/index"
    import pagination from '../../../components/pagination'
    import list from '../../../components/list/list'
    import user_post_item from '../../../components/list/item/user_post_item'

    export default {
        data() {
            return {
                pickerOptions: {
                    shortcuts: [{
                        text: '最近一周',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
                            picker.$emit('pick', [start, end])
                        }
                    }, {
                        text: '最近一个月',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
                            picker.$emit('pick', [start, end])
                        }
                    }, {
                        text: '最近三个月',
                        onClick(picker) {
                            const end = new Date()
                            const start = new Date()
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
                            picker.$emit('pick', [start, end])
                        }
                    }]
                },
                form: {
                    ordering: null,
                    search: null,
                    post_category: null,
                    created_time_range: [],
                },
                params: {
                    limit: 10,
                    offset: 0,
                    name: null,
                    start_created_time: null,
                    end_created_time: null,
                    category: null,
                    ordering: null,
                    post_type: 1,
                },
                posts: {
                    total: 0,
                    results: null
                }
            }
        },
        mounted() {
            this._get_user_posts()
        },
        methods: {
            update_post(post) {
                // 用户按下编辑按钮时
                this.blank_push({
                    'name': 'postings_detail',
                    'params': {id: post.id}
                })
            },
            async delete_post(post) {
                //用户按下删除按钮时
                let res = await api_user_post.destory(post.id)
                res = res.data
                if (res.code !== 2000) {
                    return this.$message(res.msg)
                }
                // eslint-disable-next-line require-atomic-updates
                post.status = 1
            },
            filter_post() {
                // 点击查询
                if (this.form.created_time_range) {
                    this.params.start_created_time = this.form.created_time_range[0]
                    this.params.end_created_time = this.form.created_time_range[1]
                } else {
                    this.params.start_created_time = null
                    this.params.end_created_time = null
                }
                if (this.form.post_category) {
                    this.params.category = this.form.post_category[this.form.post_category.length - 1]
                } else {
                    this.params.category = null
                }
                this.params.ordering = this.form.ordering
                this.params.search = this.form.search
                this._get_user_posts()
            },
            async _get_user_posts() {
                this.move_to_top()
                // 获取用户个人帖子
                let loading = this.openLoading({
                    target: '.my_post'
                })
                let res = await api_user_post.list(this.params)
                res = res.data
                if (res.code !== 2000) {
                    this.$message(res.msg)
                    loading.close()
                    return
                }
                this.posts = res.data
                loading.close()
            },
        },
        computed: {
            ...mapState(['option'])
        },
        components: {
            pagination,
            list,
            user_post_item
        },
        inject: ['blank_push', 'move_to_top']
    }
</script>

<style scoped lang="scss">
    .v-enter, .v-leave-to {
        opacity: 0;
        transform: translateX(-60px);
    }

    .v-enter-active,
    .v-leave-active {
        transition: all 0.6s ease;
    }

    .my_post {
        text-align: left;

        .header-filter {
            padding: 0 20px;
            margin: 0 0 1em 0;
        }

        .footer-pagination {
            padding: 8%;
            text-align: center;
        }

    }

</style>
