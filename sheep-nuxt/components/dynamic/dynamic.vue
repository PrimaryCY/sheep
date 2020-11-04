<template>
    <div class="dynamic-wrap">
        <el-timeline>
            <el-timeline-item
                    v-for="d in results"
                    :key="d.created_time"
                    :timestamp="d.created_time"
                    placement="top">
                <el-card
                        class="dynamic-el"
                        v-for="dynamic in d.data"
                        :key="dynamic.id">
                    <div v-if="dynamic.action === 1"
                         class="dynamic">
                        {{created_time_format(dynamic.created_time)}}
                        <span class="dynamic-keyword">{{dynamic.show_data}}</span>
                        加入了羊绒衫!
                    </div>
                    <div v-else-if="dynamic.action === 2"
                         class="dynamic">
                        {{created_time_format(dynamic.created_time)}} 使用
                        <span class="dynamic-keyword">{{dynamic.show_data}}</span>
                        在ip:<span> {{dynamic.ip}}</span> 登录
                    </div>
                    <div v-else-if="dynamic.action === 3"
                         class="dynamic">
                        {{created_time_format(dynamic.created_time)}} 发布
                        <a :href="$router.resolve({name:'post_detail',params:{id:dynamic.show_data.id}}).href"
                           class="dynamic-keyword pointer">
                            {{dynamic.show_data.name}}
                        </a>
                    </div>
                    <div v-else-if="dynamic.action === 4"
                         class="dynamic">
                        {{created_time_format(dynamic.created_time)}} 更新
                        <a :href="$router.resolve({name:'post_detail',params:{id:dynamic.show_data.id}}).href"
                           class="dynamic-keyword pointer">
                            {{dynamic.show_data.name}}
                        </a>
                    </div>
                    <div v-else-if="dynamic.action === 5"
                         class="dynamic">
                        {{created_time_format(dynamic.created_time)}} 在 {{post_type_text(dynamic.show_data.post_type)}}
                        <a :href="dynamic.show_data.status === 0  ?
                         $router.resolve({name:'post_detail',params:{id:dynamic.show_data.id}}).href: 'javascript:;'"
                           class="dynamic-keyword pointer">
                            {{dynamic.show_data.name}}
                        </a>
                        留下了评论
                    </div>
                    <div v-else-if="dynamic.action === 6"
                         class="dynamic">
                        <div v-if="dynamic.extra_type === 1"
                             class="dynamic">
                            {{created_time_format(dynamic.created_time)}} 点赞了 {{post_type_text(dynamic.show_data.post_type)}}
                            <a :href="dynamic.show_data.status === 0  ?
                            $router.resolve({name:'post_detail',params:{id:dynamic.show_data.id}}).href: 'javascript:;'"
                               class="dynamic-keyword pointer">
                                {{dynamic.show_data.name}}
                            </a>
                        </div>
                        <div v-else-if="dynamic.extra_type === 2"
                             class="dynamic">
                            {{created_time_format(dynamic.created_time)}} 点赞了
                            <span class="dynamic-keyword">
                                {{dynamic.show_data.user.username}}
                            </span>
                             在 {{post_type_text(dynamic.show_data.post_type)}}
                            <a :href="dynamic.show_data.status === 0 ?
                            $router.resolve({name:'post_detail',params:{id:dynamic.show_data.id}}).href: 'javascript:;'"
                               class="dynamic-keyword pointer">
                                {{dynamic.show_data.name}}
                            </a>
                            下的评论
                        </div>
                    </div>
                </el-card>

            </el-timeline-item>
        </el-timeline>
    </div>
</template>

<script>
import {dateFormat} from '@/utils/util'

export default {
    name: "dynamic",
    props:{
        results:{
            type:Array,
            required:true
        }
    },
    data(){
        return{
        }
    },
    methods:{
        post_type_text(post_type){
            return post_type === 1 ? '文章':'提问'
        },
        created_time_format(time){
            let date = new Date(time)
            return dateFormat("HH:MM:SS", date)
        }
    }
}
</script>

<style scoped lang="scss">
.dynamic-wrap {
    margin-top: 2em;
    width: 90%;
    text-align: left;
    .el-timeline{
        margin-left: 15%;
    }
    .dynamic-el{
        margin-top: 20px;
        .dynamic{
            font-weight: 800;
            .dynamic-keyword{
                font-weight: 900;
                color: #b53c57;
                text-decoration:none;
                border-bottom: 1px solid #b53c57;
            }
            .dynamic-keyword:hover{
            }
        }
    }
}
</style>
