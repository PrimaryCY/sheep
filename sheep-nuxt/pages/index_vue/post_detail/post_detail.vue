<template>
    <div class="wrap">
        <div class="left" :style="{'margin-right':pack_up?'150px':'190px'}">
            <div v-if="not_found_page">
                404
            </div>
            <div class="article" v-else-if="data.post_type===1">
                <div class="article-title">
                    <h1>
                        {{data.name}}
                    </h1>
                    <div class="article-info"
                         :class="{'is_fixed' : isFixed}"
                         id="boxFixed">
                        <el-row type="flex">
                            <el-col :span="2">
                                <div class="on cancel-select">
                                    <svg class="icon-mid" aria-hidden="true">
                                        <use xlink:href="#icon-liulan"></use>
                                    </svg>
                                    <span>
                      {{data.read_num}}
                    </span>
                                </div>
                            </el-col>
                            <el-col :span="4">
                                <div class="on cancel-select">
                                    <star
                                            ref="praise"
                                            animate="animated bounceIn"
                                            color="#b53c57">
                                        <svg class="icon-mid pointer compatibility-icon" slot="icon"
                                             @click="click_praise_or_tread(1)"
                                             aria-hidden="true">
                                            <use xlink:href="#icon-icon_likegood"></use>
                                        </svg>
                                    </star>
                                    <span>&nbsp;{{data.praise_num}}&nbsp;</span>
                                    <star
                                            ref="tread"
                                            animate="animated bounceIn"
                                            color="#b53c57">
                                        <svg class="icon-mid pointer compatibility-icon"
                                             slot="icon"
                                             @click="click_praise_or_tread(-1)"
                                             aria-hidden="true">
                                            <use xlink:href="#icon-cai-copy"></use>
                                        </svg>
                                    </star>
                                </div>
                            </el-col>
                            <el-col :span="2">
                                <div class="on cancel-select">
                                    <svg class="icon-mid compatibility-icon"
                                         aria-hidden="true">
                                        <use xlink:href="#icon-icon_community_line"></use>
                                    </svg>
                                    <span>
                      {{data.post_num}}
                    </span>
                                </div>
                            </el-col>
                            <el-col :span="2">
                                <div class="on cancel-select">
                                    <star
                                            ref="like"
                                            animate="animated bounceIn"
                                            color="#b53c57">

                                        <el-popover
                                                placement="bottom"
                                                slot="icon"
                                                popper-class="clear-padding"
                                                v-model="like_dialog"
                                                :visible-arrow="false"
                                                @click.native.stop="click_like"
                                                width="260">
                                            <div class="like-dialog">
                                                <div class="list">
                                                    <el-row
                                                            class="item pointer"
                                                            :class="{is_like:i.is_like}"
                                                            type="flex"
                                                            tabindex="0"
                                                            @click.native="add_or_del_like(i)"
                                                            v-for="i in collect" :key="i.id">
                                                        <el-col :span="3">
                                                            <img :src="i.image">
                                                        </el-col>
                                                        <el-col :span="15" :offset="1">
                                                            <div class="ellipsis" style="margin-bottom: 5px">
                                                                {{i.name}}
                                                            </div>
                                                            <font_icon v-if="i.is_show" :type="5">
                                                            </font_icon>
                                                            <font_icon v-else :type="6">
                                                            </font_icon>
                                                        </el-col>
                                                        <el-col :span="6">
                                                            <div class="ellipsis" style="text-align: center">
                                                                <el-rate
                                                                        :value="Number(i.is_like)"
                                                                        disabled
                                                                        :colors="{1:'#b53c57'}"
                                                                        show-score
                                                                        :score-template="`${i.total}`"
                                                                        :max="1">
                                                                </el-rate>
                                                            </div>
                                                        </el-col>
                                                    </el-row>
                                                </div>
                                                <div class="add-like-category">
                                                    <el-button v-show="!collect_form.flag"
                                                               size="mini"
                                                               type="text"
                                                               @click="click_add_category_btn">
                                                        新增收藏集
                                                    </el-button>
                                                    <div v-show="collect_form.flag">
                                                        <el-row type="flex">
                                                            <el-col :span="18">
                                                                <el-input size="mini"
                                                                          class="like-input"
                                                                          ref="like-input"
                                                                          placeholder="输入收藏集名称..."
                                                                          v-model="collect_form.name"
                                                                          @keyup.enter.native="create_like_category"
                                                                          type="text"></el-input>
                                                            </el-col>
                                                            <el-col :span="6">
                                                                <el-button size="mini"
                                                                           type="text"
                                                                           :disabled="collect_form.name.length===0"
                                                                           @click="create_like_category">
                                                                    新增
                                                                </el-button>
                                                            </el-col>
                                                        </el-row>
                                                    </div>
                                                </div>
                                            </div>
                                            <svg
                                                    slot="reference"
                                                    class="icon-mid compatibility-icon pointer"
                                                    aria-hidden="true">
                                                <use xlink:href="#icon-shoucang1"></use>
                                            </svg>
                                        </el-popover>
                                    </star>
                                    <span>
                      {{data.like_num}}
                    </span>
                                </div>
                            </el-col>
                            <el-col :span="5" :offset="5">
                <span class="byline">
                  分类:{{data.category}}
                </span>
                            </el-col>
                            <el-col :span="1">
                                <div class="divider">
                                    |
                                </div>
                            </el-col>
                            <el-col :span="5">
                <span class="byline">
                  发布于&nbsp;{{data.created_time}}
                </span>
                            </el-col>
                        </el-row>
                        <el-divider></el-divider>
                    </div>
                </div>
                <div class="article-content-wrap">
                    <div class="article-content" v-html="data.html_content">
                    </div>
                    <div class="updatetime-text">
                        -------------&nbsp;&nbsp;&nbsp;最后更新于&nbsp;{{data.update_time}}
                    </div>
                </div>
                <div class="divider-line">
                    <el-divider></el-divider>
                </div>
                <div class="article-reply">
                   <reply_input
                           :avatar="user.portrait"
                   >
                   </reply_input>

                    <a-list
                            class="reply-list"
                            :header="`共 ${comments.length} 条`"
                            item-layout="horizontal"
                            :locale="{emptyText: '暂无评论'}"
                            :data-source="comments"
                            :loading="comments.loading"
                    >
                        <a-list-item slot="renderItem" slot-scope="item">

                            <a-comment :author="item.author" :avatar="item.avatar">
                                <template slot="actions">
                                    <span @click="comments_input=item.id">回复</span>
                                </template>
                                <div slot="content">
                                    {{ item.content }}
                                </div>
                                <a-tooltip slot="datetime" :title="item.datetime.format('YYYY-MM-DD HH:mm:ss')">
                                    <span>{{ item.datetime.fromNow() }}</span>
                                </a-tooltip>

                                <a-comment>
                                    <span slot="actions">
                                        <div @click="comments_input=item.id">
                                            回复
                                        </div>
                                    </span>
                                    <a slot="author">回复标题</a>
                                    <a-avatar
                                            slot="avatar"
                                            src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                                            alt="Han Solo"
                                    />
                                    <div slot="content">
                                        We supply a series of design principles, practical patterns and high quality
                                        design
                                        resources (Sketch and Axure).
                                    </div>
                                    <reply_input
                                            :avatar="user.portrait"
                                            :reply_name="item.author"
                                            v-show="comments_input===item.id">
                                    </reply_input>
                                </a-comment>
                                <reply_input
                                        :avatar="user.portrait"
                                        :reply_name="item.author"
                                        v-show="comments_input===item.id">
                                </reply_input>
                            </a-comment>
                        </a-list-item>
                    </a-list>


                </div>

            </div>
            <div v-else-if="data.post_type===2"></div>
        </div>
        <div class="right">
            <div class="author-info-wrap" v-if="!not_found_page">
                <a class="ellipsis author-info pointer">
                    <el-avatar
                            class="vertical-middle"
                            :size="60"
                            :src="data.author_info.portrait">
                    </el-avatar>
                    <h1 class="username">
                        <svg v-if="data.author_info.gender===0" class="icon-min" aria-hidden="true">
                            <use xlink:href="#icon-xingbienv-copy"></use>
                        </svg>
                        <svg v-else class="icon-min" aria-hidden="true">
                            <use xlink:href="#icon-xingbienan-copy"></use>
                        </svg>
                        :
                        {{data.author_info.username}}
                    </h1>
                </a>
                <p>
                    <svg class="icon-min" aria-hidden="true">
                        <use xlink:href="#icon-nianling"></use>
                    </svg>
                    :
                    {{data.author_info.age}}
                </p>
                <span>网站年龄: {{data.author_info.website_age}}</span>
            </div>
            <div class="list-wrap">
                <post_detail_list
                        v-if="author_post.results"
                        :list="author_post.results"
                        :bottom="false"
                        title="他的文章">
                    <template v-slot:item-content="data">
                        <post_detail_item :post="data.item">

                        </post_detail_item>
                    </template>
                </post_detail_list>
            </div>
            <div class="list-wrap">
                <post_detail_list
                        :list="category_post.results"
                        :bottom="false"
                        title="推荐文章">
                    <template v-slot:item-content="data">
                        <post_detail_item :post="data.item">

                        </post_detail_item>
                    </template>
                </post_detail_list>

            </div>
        </div>
    </div>
</template>

<script>
    import moment from 'moment'
    import {mapState} from 'vuex'

    import {
        api_post,
        api_category_post,
        api_user_collect,
        api_user_collect_category,
        api_correlation_category,
        api_user_praise,
        api_author_post
    } from '../../../api'
    import reply_input from "../../../components/reply/reply_input"
    import post_detail_list from '../../../components/list/post-detail-list'
    import post_detail_item from '@/components/list/item/post-detail-item'
    import font_icon from '@/components/small/font_icon'
    import star from '@/components/common/star'
    import {get_tree_first_node} from '../../../utils/util'


    export default {
        head: {
            link: [
                {res: "stylesheet", type: 'text/css', href: "http://biger.applinzi.com/api/css/animate.min.css"}
            ]
        },
        name: 'post_detail',
        data() {
            return {
                comments_input:0,
                comments: [             //评论内容
                    {
                        id:1,
                        author: 'Han Solo',
                        avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png',
                        content:
                            'We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.',
                        datetime: moment().subtract(1, 'days'),
                    },
                    {
                        id:2,
                        author: 'li SI',
                        avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png',
                        content:
                            'We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.',
                        datetime: moment().subtract(2, 'days'),
                    },
                ],
                moment,
                response: {    //文章内容具体响应,包含code值
                },
                data: {        // 文章内容
                    author_info: {}
                },
                reply_form: {  //评论
                    placeholder: '请输入回复内容...',
                    html_content: ''
                },
                correlation_category: {  //相关分类
                    results: []
                },
                author_post: {       //作者其它文章
                    results: []
                },
                category_post: {     //相同分类下文章
                    results: []
                },
                collect: [],        //用户收藏类别列表
                collect_form: {    //新增收藏集表单
                    name: '',
                    flag: false      //是否展示新增类别输入框
                },
                isFixed: false,    //吸顶
                offsetTop: 0,     //吸顶
                not_found_page: false, //是否展示404页面
                like_dialog: false,    // 点击收藏的dialog
            }
        },
        components: {
            post_detail_list,
            post_detail_item,
            star,
            font_icon,
            reply_input
        },
        computed: {
            ...mapState(['pack_up', 'user']),
        },
        inject: ['blank_push'],
        async asyncData(context) {
            let id, post_res, detail_recommend_list
            id = context.params.id
            let return_dict = {}
            try {
                post_res = await api_post.retrieve(id)
                post_res = post_res.data

                return_dict['data'] = post_res.data ? post_res.data : {}
                return_dict['response'] = post_res
                if (post_res.code === 404) {
                    return_dict['not_found_page'] = true
                } else {
                    let corr_res, au_post_res, cate_post_res
                    detail_recommend_list = [
                        // 相关分类
                        api_correlation_category.list({id: post_res.data.category_id}),
                        // 作者相关文章
                        api_author_post.list({author_id: post_res.data.author_id, limit: 5}),
                        // 相关分类文章
                        api_category_post.list({category: post_res.data.category_id, limit: 5})
                    ];
                    [corr_res, au_post_res, cate_post_res] = await Promise.all(detail_recommend_list)
                    return_dict['correlation_category'] = corr_res.data.data
                    return_dict['author_post'] = au_post_res.data.data
                    return_dict['category_post'] = cate_post_res.data.data
                }
            } catch (e) {
                context.error({statusCode: 500, message: 'ssr internal server error'})
            }
            return return_dict
        },
        methods: {
            async click_praise_or_tread(flag) {
                // 用户点赞与点踩
                console.log(flag)
                let data = {
                    t: 1,
                    resource_id: this.data.id
                }
                if (this.data.is_praise === flag) {
                    console.log('取消点赞/踩')
                    data['praise_or_trample'] = 0
                    let res = await api_user_praise.create(data)
                    res = res.data
                    if (res.code !== 2000) return
                    this.data.praise_num += res.data.return_num
                    this.custom_notify(res.data.msg)
                    this.data.is_praise = 0
                } else if (flag === 1) {
                    if (this.$refs['tread'].active) {
                        this.$refs['tread'].toggle()
                    }
                    console.log('点赞')
                    data['praise_or_trample'] = 1
                    let res = await api_user_praise.create(data)
                    res = res.data
                    if (res.code !== 2000) return
                    this.data.praise_num += res.data.return_num
                    this.custom_notify(res.data.msg)
                    this.data.is_praise = 1

                } else if (flag === -1) {
                    if (this.$refs['praise'].active) {
                        this.$refs['praise'].toggle()
                    }
                    console.log('踩')
                    data['praise_or_trample'] = -1
                    let res = await api_user_praise.create(data)
                    res = res.data
                    if (res.code !== 2000) return
                    this.data.praise_num += res.data.return_num
                    this.custom_notify(res.data.msg)
                    this.data.is_praise = -1
                }
            },
            async add_or_del_like(category) {
                // 用户收藏与取消收藏
                let res = await api_user_collect.create({
                    resource_id: this.data.id,
                    category_id: category.id,
                })
                res = res.data
                if (res.code !== 2000) {
                    return this.custom_notify(res.msg)
                }
                // eslint-disable-next-line require-atomic-updates
                category.is_like = !category.is_like
                this.custom_notify(res.data)
                if (category.is_like) {
                    category.total++
                    this.data.like_num++
                    this.data.is_like = true
                } else {
                    category.total--
                    this.data.like_num--
                    let flag
                    for (let i of this.collect) {
                        if (i.is_like) {
                            flag = true
                            break
                        }
                        flag = false
                    }
                    this.data.is_like = flag
                }
                this.like_dialog = !this.like_dialog
            },
            async click_like() {
                // 点击收藏星星图标
                if (!this.user.username) {
                    this.like_dialog = false
                    const h = this.$createElement
                    return this.$msgbox({
                        title: '收藏👋',
                        message: h('p', null, [
                            h('i', {style: 'color: teal'}, '未登录用户暂不可以收藏🙈')
                        ]),
                        showCancelButton: true,
                        confirmButtonText: '现在去登录➡️',
                        cancelButtonText: '取消',
                    }).then(() => {
                        return this.blank_push({
                            'name': 'login', 'query': {
                                from: this.$route.path
                            }
                        })
                    }).catch(() => {
                    })
                }
                let collect = await api_user_collect_category.list({
                    resource_id: this.data.id,
                    type: 1
                })
                collect = collect.data
                if (collect.code !== 2000) {
                    this.custom_notify(collect.msg)
                    this.like_dialog = false
                    return null
                }
                this.collect = collect.data
            },
            custom_notify(msg) {
                this.$notify({
                    message: `<strong>${msg}</strong>`,
                    dangerouslyUseHTMLString: true,
                    showClose: true,
                })
            },
            async create_like_category() {
                let loading = this.openLoading({
                    text: '创建中...',
                    target: '.like-dialog'
                })
                let res = await api_user_collect_category.create(this.collect_form)
                res = res.data
                if (res.code !== 2000) {
                    loading.close()
                    return this.custom_notify(res.msg)
                }
                this.collect_form.name = ''
                this.collect_form.flag = !this.collect_form.flag
                this.collect.unshift(res.data)
                loading.close()
            },
            initHeight() {
                // 文章顶部栏吸顶效果
                var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
                this.isFixed = scrollTop - 15 > this.offsetTop ? true : false
                let el = document.getElementById('boxFixed')
                if (!el) return null
                if (this.isFixed) {
                    let width = document.getElementsByClassName('left')[0].clientWidth
                    el.style.width = `${width}px`
                } else {
                    el.style.width = 'initial'
                }
            },
            async _get_404_data() {
                if (process.server) {
                    return null
                }
                if (this.not_found_page) {
                    let c, corr_res, cate_post_res
                    c = get_tree_first_node(this.$store.state.option.post_category);
                    [corr_res, cate_post_res] = await Promise.all([
                        api_correlation_category.list({id: c}),
                        api_category_post.list({category: c})
                    ])
                    this.correlation_category = corr_res.data.data
                    this.category_post = cate_post_res.data.data
                }
            },
            _pre_like_praise() {
                // 页面加载预处理点赞状态收藏状态
                if (!this.$refs['like']) return
                this.$refs['like'].status = this.data.is_like
                if (this.data.is_praise === 1) {
                    this.$refs['praise'].status = true
                } else if (this.data.is_praise === -1) {
                    this.$refs['tread'].status = true
                }
            },
            click_add_category_btn() {
                // 点击新增收藏集按钮
                this.collect_form.flag = !this.collect_form.flag
                this.$nextTick(() => {
                    this.$refs['like-input'].focus()
                })
            },
        },
        async created() {
            await this._get_404_data()
            this._pre_like_praise()
        },
        mounted() {
            window.addEventListener('scroll', this.initHeight)
            this.$nextTick(() => {
                let el = document.querySelector('#boxFixed')
                if (el) this.offsetTop = el.offsetTop
            })
        },
        destroyed() {
            window.removeEventListener('scroll', this.handleScroll)
        },
        watch: {
            "data.is_like": {
                deep: true,
                handler: function (n) {
                    if (!this.$refs['like']) return
                    this.$refs['like'].status = n
                }
            },
        }
    }
</script>

<style scoped lang="scss">

    .like-dialog {
        font-size: 12px;
        text-align: left;
        margin-top: 6px;

        .add-like-category {
            text-align: center;

            font-size: 12px;
            border-top: 1px solid #EBEEF5;

            button {
                height: 35px;
                color: #d2d2d2;
            }

            .like-input {
                height: 100%;

                /deep/ input {
                    height: 100% !important;
                }
            }
        }

        .list {
            max-height: 300px;
            overflow-y: auto;
            padding-bottom: 35px;

            .item {
                padding: 8px 10px;
                outline: 0;

                img {
                    width: 30px;
                    height: 30px;
                    vertical-align: middle;
                }
            }

            .is_like {
                background-color: #ecf5ff;
            }

            .item:hover {
                background-color: #f5f7fa;
            }

            /*.item:focus{*/
            /*outline: -webkit-focus-ring-color auto 1px;*/
            /*}*/
        }

        .add-like-category:hover {
            button {
                color: #007fff;
            }
        }

    }

    /* 吸顶 */
    .is_fixed {
        position: fixed;
        top: 0;
        z-index: 999;
        margin: 0;
        padding: 0 !important;
        background-color: white;

        .el-divider--horizontal {
            margin-top: 5px;
            margin-bottom: initial !important;
        }
    }

    /*更新日期文字样式*/
    .updatetime-text {
        font-size: 12px;
        text-align: right;
        font-weight: 600;
        color: #999;
    }

    .el-divider--horizontal {
        margin-top: 5px;
    }

    .wrap {
        position: initial !important;
        height: 100%;

        .left {
            height: 100%;
            /*margin-right: 180px;*/
            margin-left: -30px;

            .article {
                .article-title {
                    padding: 10px 0;

                    h1 {
                        font-size: 28px;
                        word-wrap: break-word;
                        color: #222226;
                        line-height: 33px;
                        font-weight: 600;
                        margin: 0;
                        word-break: break-all;
                    }

                    .article-info {
                        font-size: 11px;

                        .on {
                            height: 30px;
                            margin-top: 1em;

                            svg {
                                vertical-align: bottom;
                            }

                            span {
                                display: inline-block;
                                min-width: 20px;
                            }

                            .compatibility-icon {
                                margin-top: 2px;
                                width: 18px;
                                height: 18px;
                                vertical-align: sub;
                            }
                        }

                        .byline {
                            text-align: right;
                            font-weight: 600;
                        }

                        .divider {
                            margin-top: 1em;
                            line-height: 100%;
                            font-size: 15px;
                            text-align: right;
                        }

                        .num_data {
                            border-radius: 25%;
                        }

                        .num_data:hover {
                            background-color: #ecf5ff;
                        }
                    }
                }

                .article-content-wrap {
                    text-align: initial;

                    .article-content {
                        min-height: 60vh;

                        * {
                            font-size: initial;
                            margin: initial;
                            border: initial;
                            font-weight: initial;
                            vertical-align: initial;
                        }
                    }
                }

                .article-reply {
                    text-align: right;
                    .reply-list{
                        text-align: left;
                        width: 100%;
                    }
                }
            }
        }

        .right {
            position: absolute;
            right: 0;
            top: 0;
            width: 240px;
            border-left: 1px ridge rgba(150, 150, 150, 0.1);

            .author-info-wrap {
                border-bottom: 1px solid #EBEEF5;
                /*border-left: 1px solid #EBEEF5;*/
                margin-top: 40px;
                padding-bottom: 20px;

                .author-info {
                    color: #1a1a1a;
                    font-weight: 500;

                    h1 {
                        margin: 10px;
                    }
                }
            }

            .list-wrap {
                text-align: initial;
            }
        }
    }

</style>
