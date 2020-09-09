<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <div class="my_post">
        <div class="header-filter">
            <el-form  label-position="left">
                <el-row type="flex" :gutter="20">
                    <el-col :span="12">
                        <el-form-item
                                label-width="75px"
                                label="点赞日期:">
                            <el-date-picker
                                    v-model="form.update_time_range"
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
                            <el-select	v-model="form.praise_or_trample"
                                          clearable
                                          size="small"
                                          placeholder="请选择">
                                <el-option
                                        label="点赞"
                                        value="1"
                                ></el-option>
                                <el-option
                                        label="点踩"
                                        value="-1"
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
                <common_post_item
                        :post="data.item"
                        >
                </common_post_item>
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
    import {api_user_praise} from "@/api/index"
    import pagination from '../../../components/pagination'
    import list from '../../../components/list/list'
    import common_post_item from '../../../components/list/item/common_post_item'
    import {pickerOptions} from '../../../utils/util'

    export default {
        data() {
            return {
                pickerOptions: pickerOptions,
                form:{
                    praise_or_trample:null,
                    update_time_range:[],
                },
                params:{
                    limit:10,
                    offset:0,
                    start_created_time:null,
                    end_created_time:null,
                    praise_or_trample:null,
                    t:1,
                },
                posts:{
                    total:0,
                    results:null
                }
            }
        },
        mounted() {
            this._get_user_posts()
        },
        methods:{
            filter_post(){
                // 点击查询
                if(this.form.update_time_range){
                    this.params.start_update_time=this.form.update_time_range[0]
                    this.params.end_update_time=this.form.update_time_range[1]
                }else{
                    this.params.start_update_time=null
                    this.params.end_update_time=null
                }

                this.params.praise_or_trample = this.form.praise_or_trample
                this._get_user_posts()
            },
            async _get_user_posts(){
                this.move_to_top()
                // 获取用户个人帖子
                let loading = this.openLoading({
                    target:'.my_post'
                })
                let res = await api_user_praise.list(this.params)
                res = res.data
                if(res.code!==2000){
                    this.$message(res.msg)
                    return loading.close()
                }
                this.posts=res.data
                loading.close()
            },
        },
        components:{
            pagination,
            list,
            common_post_item
        },
        inject:['blank_push', 'move_to_top']
    }
</script>

<style scoped lang="scss">
    .v-enter,.v-leave-to{
        opacity: 0;
        transform: translateX(-60px);
    }
    .v-enter-active,
    .v-leave-active{
        transition: all 0.6s ease;
    }

    .my_post{
        text-align: left;
        .header-filter{
            padding: 0 20px;
            margin: 0 0 1em 0;
        }

        .footer-pagination{
            padding: 8%;
            text-align: center;
        }

    }

</style>
