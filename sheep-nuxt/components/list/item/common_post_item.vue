<template>
    <div
            class="article-list-item-mp">
        <div
                class="article-list-item-warp">
            <el-row class="article-title">
                <el-col>

                    <div class="image-title-warp">
                        <div v-show="post.image" class="article-image">
                            <img :src="post.image">
                        </div>
                        <!--未被删除的文章才可以点击跳转-->
                        <a v-if="post.status === 0"
                           :href="$router.resolve({name:'post_detail',params:{id:post.id}}).href"
                           target="_blank"
                           :class="{'article-image-title-text':post.image}"
                           class="article-title-text two-line-ellipsis">
                            <font_icon :type="post.post_type"></font_icon>
                            {{ post.name }}
                        </a>
                        <a
                                v-else
                                href="#"
                                :class="{'article-image-title-text':post.image}"
                                class="article-title-text two-line-ellipsis">
                            <font_icon :type="post.post_type"></font_icon>
                            {{ post.name }}
                        </a>
                        <span class="article-desc byline ellipsis">
              {{ post.desc }}
            </span>
                    </div>
                </el-col>
            </el-row>
            <el-row class="article-info">
                <el-col :span="3">
                    <a class="ellipsis author-info">
                        <el-avatar
                                class="vertical-middle"
                                size="small"
                                :src="post.author_info.portrait">
                        </el-avatar>
                        {{ post.author_info.username }}
                    </a>
                </el-col>
                <el-col :span="5">
                    {{ post.post_type === 1 ? '发布于' : '提问于' }}:{{ moment(post.created_time).fromNow() }}
                    &nbsp;
                </el-col>
                <!--        <el-col :span="1">-->
                <!--占位使用:恭喜发财-->
                <!--        </el-col>-->
                <el-col :span="2">
                    <svg class="icon-min" aria-hidden="true">
                        <use xlink:href="#icon-liulan"></use>
                    </svg>
                    :{{ post.read_num }}
                </el-col>
                <el-col :span="2">
                    <svg class="icon-min" aria-hidden="true">
                        <use :xlink:href="post.praise_num < 0 ? '#icon-cai-copy':'#icon-icon_likegood'"></use>
                    </svg>
                    :{{ post.praise_num }}
                </el-col>
                <el-col :span="2">
                    <svg class="icon-min" aria-hidden="true">
                        <use xlink:href="#icon-shoucang"></use>
                    </svg>
                    :{{ post.like_num }}
                </el-col>
                <el-col :span="2">
                    <svg class="icon-min" aria-hidden="true">
                        <use xlink:href="#icon-icon_community_line"></use>
                    </svg>
                    :{{ post.post_num }}
                </el-col>
                <el-col :span="2">
                    <!--占位使用-->
                </el-col>
                <!--被删除的文章会有已被删除的提示语-->
                <el-col v-if="post.status === 0 && post.newest_user_id" :span="6">
                    <div class="reply-txt ellipsis">
                        {{ moment(post.newest_time).fromNow() }} • 最后回复来自于&nbsp;{{ post.newest_user_info.username }}
                    </div>
                </el-col>
                <el-col v-if="post.status !== 0" :span="6" class="delete_msg">
                    {{ `此${post.post_type === 1 ? '文章' : '问题'}已被删除!` }}
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
import moment from '@/utils/moment'
import font_icon from '../../small/font_icon'

export default {
    name: 'post_item',
    data() {
        return {
            moment
        }
    },
    props: {
        post: {
            type: Object,
            required: true
        },
    },
    components: {
        font_icon
    },
}
</script>

<style scoped lang="scss">
.article-list-item-mp {
    text-align: initial;

    .article-list-item-warp {
        color: black;
        display: block;
    }
}

.article-title {
    -webkit-box-orient: horizontal;
    -ms-flex-direction: row;
    flex-direction: row;
    -webkit-box-pack: start;
    -ms-flex-pack: start;
    justify-content: flex-start;

    .image-title-warp {
        position: relative;

        .article-image {
            position: absolute;
            display: inline-block;

            img {
                vertical-align: text-top;
                width: 100px;
                height: 45px;
                object-fit: cover;
                border-radius: 5px;
            }
        }

        .article-image-title-text {
            margin-left: 105px;
            min-height: 46px;
        }

        .article-title-text {
            font-size: 14px;
            font-weight: bold;
            color: #4d4d4d;
            margin-bottom: 0;
            -webkit-box-flex: 1;
            -ms-flex-positive: 1;
            flex-grow: 1;
        }

        .article-desc {
            font-size: 10px !important;
            display: -webkit-box;
            margin-top: initial;
        }

        .article-title-text:hover {
            color: #b53c57;
        }
    }
}

.article-info {
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

    .reply-txt {
        text-align: right;
    }

    .author-info {
        color: #1a1a1a;
        font-weight: 500;
    }

    .delete_msg {
        border: 0 !important;
        color: #F56C6C;
        text-align: center;
    }
}

</style>
