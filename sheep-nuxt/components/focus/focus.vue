<template>
    <div class="focus-wraps">
        <ul class="focus-content">
            <li v-for="user in data" class="focus" :key="user.id">
                <div class="focus-portrait">
                    <el-avatar
                            class="vertical-middle"
                            :size="60"
                            :src="user.portrait">
                    </el-avatar>
                </div>
                <div class="focus-info">
                    <div class="focus-username ellipsis">
                        {{user.username}}
                    </div>

                    <p class="focus-brief ellipsis">
                        {{user.brief}}
                    </p>

                </div>

                <div class="focus-delete" v-if="schema === 'focus'">
                    <el-popconfirm
                            confirmButtonText='是的'
                            cancelButtonText='不用了'
                            icon="el-icon-info"
                            iconColor="red"
                            @onConfirm="click_focus(user)"
                            title="确定取消关注该用户吗？"
                    >
                        <el-button type="danger"
                                   icon="el-icon-close"
                                   circle
                                   slot="reference"
                                   size="small"
                                   :loading.sync="focus_loading[user.id]"
                                   ></el-button>
                    </el-popconfirm>
                </div>
            </li>
        </ul>

        <not_data text="空空如也..."
                  :list="data"></not_data>
    </div>
</template>

<script>
import {api_user_focus} from "@/api"
import not_data from './../not_data'


export default {
    name: "focus",
    data(){
        return{
            focus_loading:{}
        }
    },
    props:{
        // 有focus和fans两种mode
        schema: {
            type: String,
            required: true
        },
        data:{
            type: Array,
            required: true
        }
    },
    methods:{
        async click_focus(user) {
            // 取消关注
            this.focus_loading[user.id] = true
            let res = await api_user_focus.create({focus_id: user.id})
            res = res.data
            if(res.code !== 2000){
                this.loading[user.id] = false
                return this.$message(res.msg)
            }
            await this.sleep(0.5)
            this.data.splice(this.data.indexOf(user), 1)
        },
    },
    components:{
        not_data
    }
}
</script>

<style scoped lang="scss">
.focus-wraps {
    .focus-content {
        padding: 2rem 1rem 0 4rem;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        flex-wrap: wrap;

        .focus {
            width: calc(23%);
            text-align: left;
            display: flex;
            margin: 0 10px 10px 10px;

            .focus-portrait{
                flex: 0 0 auto;
                padding: 10px;
            }
            .focus-info{
                flex: 1 1 auto;
                padding: 10px;
                .focus-username{
                    font-weight: bold;
                    font-size: 15px;
                    margin-top: 5px;
                }
                .focus-brief{
                    font-size: 13px;
                    color:#8a9aa9;
                }
            }
            .focus-delete{
                flex: 2 2 auto;
                text-align: center;
                button{
                    margin: 20px;
                }
            }
        }
    }
}

</style>