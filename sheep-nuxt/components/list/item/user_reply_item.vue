<template>
    <div class="item-warp"  :class="{'is-read': item.is_read}">
        <el-row class="title">
            <el-col :span="22" style="margin-left: 10px; ">
                <el-avatar
                        class="vertical-middle"
                        size="large"
                        :src="item.author_info.portrait">
                </el-avatar>
                <span v-if="item.parent_id" class="article-title-text" @click="blank_push_post_detail(item.post_info)">

                    {{ item.author_info.username }}回复了你在
                    <span class="post-name pointer"
                          @click="blank_push_post_detail(item.post_info)">{{ item.post_info.name }}</span>
                    下的评论
                </span>
                <span v-else>
                    <span v-if="item.author_id === user.id">
                        你自己回复了你自己的{{ item.post_info.post_type === 1 ? '文章' : '问题' }}
                        <span class="post-name pointer"
                              @click="blank_push_post_detail(item.post_info)">{{ item.post_info.name }}</span>
                    </span>
                    <span v-else>
                        {{ item.author_info.username }}
                        回复了你的
                        <span class="post-name pointer"
                              @click="blank_push_post_detail(item.post_info)">{{ item.post_info.name }}</span>
                    </span>
                </span>
            </el-col>
        </el-row>
        <div class="comment two-line-ellipsis">
            {{ item.content }}
        </div>
        <el-row class="info">
            <el-col :span="2">
                回复于:{{ moment(item.created_time).fromNow() }}
            </el-col>
            <el-col :span="2">
                <svg class="icon-min" aria-hidden="true">
                    <use :xlink:href="item.praise_num < 0 ? '#icon-cai-copy':'#icon-icon_likegood'"></use>
                </svg>
                :{{ item.praise_num }}
            </el-col>
        </el-row>
    </div>
</template>

<script>
import moment from '@/utils/moment'
import {mapState} from "vuex"

export default {
    name: 'user_reply_item',
    data() {
        return {
            moment
        }
    },
    props: {
        item: {
            type: Object,
            required: true
        },
    },
    methods: {
        blank_push_post_detail(post) {
            if (post.status !== 0) {
                return this.$message(`此${post.post_type === 1 ? '文章' : '问题'}已被删除!`)
            }
            this.blank_push({name: 'post_detail', params: {id: post.id}})
        }
    },
    computed: {
        ...mapState(['user'])
    },
    components: {
    },
    inject: ['blank_push'],
}
</script>

<style scoped lang="scss">

.is-read{
    color: #717181!important;
}

.item-warp {
    color: black;
    text-align: initial;
    display: block;

    .title {
        -webkit-box-orient: horizontal;
        -ms-flex-direction: row;
        flex-direction: row;
        -webkit-box-pack: start;
        -ms-flex-pack: start;
        justify-content: flex-start;

        .post-name {
            color: #007fff;
        }
    }

    .comment {
        font-size: 15px;
        margin: 20px;
        padding: 10px;
        background: #fafbfc;
        border-radius: 3px;
        border: 1px solid #f1f1f2;
    }

    .info {
        margin-top: 10px;
        display: -webkit-box;
        display: -ms-flexbox;
        font-size: 11px;
        display: flex;
        -webkit-box-orient: horizontal;
        -webkit-box-direction: normal;
        -ms-flex-direction: row;
        flex-direction: row;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -webkit-box-pack: justify;
        -ms-flex-pack: justify;
    }
}

</style>
