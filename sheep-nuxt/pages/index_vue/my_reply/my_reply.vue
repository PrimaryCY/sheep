<template>
    <div class="wrap">
        <div class="header">
            <page-heaeder
                    text="消息回复">
            </page-heaeder>
        </div>
        <el-divider>
        </el-divider>
        <div class="body">
            <div class="filter">
                <el-select v-model="params.ordering"
                           clearable
                           size="small"
                           style="margin-right: 10px"
                           @change="_get_user_reply(false)"
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
                            label="回复时间(正排序)"
                            value="created_time"
                    ></el-option>
                    <el-option
                            label="回复时间(倒排序)"
                            value="-created_time"
                    ></el-option>
                </el-select>
                <el-checkbox v-model="params.is_not_read"
                             @change="_get_user_reply(false)">未读</el-checkbox>
            </div>
            <list
                    :need_border_top="false"
                    :list="data.results">
                <template v-slot:item-content="data">
                    <user_reply_item :item="data.item">
                    </user_reply_item>
                </template>
            </list>
            <div class="footer-pagination">
                <pagination
                        @change="_get_user_reply"
                        :pagination_config="{layout:'prev, pager, next',background:true}"
                        :params="params"
                        :pager="data"></pagination>
            </div>
        </div>
    </div>
</template>

<script>
import pageHeaeder from "@/components/common/pageHeaeder"
import pagination from "@/components/pagination"
import user_reply_item from "@/components/list/item/user_reply_item"
import list from "@/components/list/list"
import {api_user_reply} from "@/api"

export default {
    name: "my_reply",
    data() {
        return {
            data: {},
            params: {},
        }
    },
    methods: {
        async _get_user_reply(move_to_top) {
            if (move_to_top) {
                this.move_to_top()
            }

            this.params.is_read = this.params.is_not_read?false:undefined
            let res = await api_user_reply.list(this.params)
            res = res.data
            if (res.code !== 2000) {
                return this.$message(res.msg)
            }
            this.data = res.data
        }
    },
    async created() {
        await this._get_user_reply()
    },
    inject: ['move_to_top'],
    components: {
        pageHeaeder,
        list,
        user_reply_item,
        pagination
    }
}
</script>

<style scoped lang="scss">
.wrap {
    .header {

    }
    .body{
        .filter{
            text-align: right;
            margin-bottom: 20px;
        }
        .footer-pagination {
            padding: 8%;
            text-align: center;
        }
    }
}
</style>