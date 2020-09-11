<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <div
            v-infinite-scroll="_get_next_posts"
            infinite-scroll-disabled="disabled_scroll"
            infinite-scroll-distance="10">
        <div class="top">
            <el-row type="flex">
                <el-col>
                </el-col>
                <el-col :span="17">
                    <el-input
                            size="mini"
                            type="text"
                            placeholder="请输入关键字"
                            v-model="form.keyword"
                            @keyup.enter.native="search"
                    ></el-input>
                </el-col>
                <el-col :span="2">
                    <div class="search-btn">
                        <el-button
                                plain
                                @click="search"
                                size="mini">
                            搜索🔍
                        </el-button>
                    </div>
                </el-col>

            </el-row>
            <div class="menuList" :class="{'is_fixed' : isFixed}" id="boxFixed">
                <ul>
                    <li :class="{active:one_category===0}">
                        <a
                                :href="$router.resolve({name:'index',query:{category:0}}).href">
                            推荐
                        </a>
                    </li>
                    <li v-for="item in option.post_category"
                        :class="{active:item.id===one_category}"
                        :key="item.id">
                        <a
                                :href="generate_url({name:'index',query:{category:item.id}})">
                            {{item.name}}
                        </a>
                    </li>
                </ul>
            </div>
            <el-carousel
                    v-if="banner.length"
                    :interval="4000"
                    type="card"
                    height="263px"
                    arrow="never">
                <el-carousel-item v-for="item in banner" :key="item.id" class="radius">
                    <a
                            target="_blank"
                            :href="generate_url({name:'post_detail',params:{id:item.id}})"
                            class="banner-wrap">
                        <img :src="item.image" class="banner-image">
                        <div class="banner-text">
                            {{item.name}}
                        </div>
                    </a>
                </el-carousel-item>
            </el-carousel>
        </div>
        <div class="content">
            <div class="left">
                <div v-if="one_category!==0">
                    <a
                            class="pointer"
                            :href="generate_url({name:'index',query:{category:one_category}})">
                        <el-tag
                                :class="{'el-tag-active':one_category===params.category}"
                                type="info"
                                size="mini">
                            全部
                        </el-tag>
                    </a>
                    <a
                            :key="c.id"
                            v-for="c in two_categories"
                            :href="generate_url({name:'index',query:{category:c.id,one_category:one_category}})"
                            class="pointer">
                        <el-tag
                                :class="{'el-tag-active':c.id===params.category}"
                                type="info"
                                size="mini">
                            {{c.name}}
                        </el-tag>
                    </a>
                </div>
                <bubble_text
                        style="margin: 20px"
                        v-if="one_category===0"
                        text="轮播图每两小时刷新，热门推荐每半小时刷新，推荐页数据每十分钟刷新🍔︎"
                        position="right">
                    <template v-slot:user>
                        <div class="dialog_reply">
                            <img src="@/static/img/admin_portrait.jpg">
<!--                            <span>小羊</span>-->
                        </div>
                    </template>
                </bubble_text>
                <bubble_text
                        style="margin: 20px"
                        v-if="one_category===0"
                        text="轮播图按点赞数，热门按浏览数，推荐页按收藏数排序🍔︎"
                        position="right">
                    <template v-slot:user>
                        <div class="dialog_reply">
                            <img src="@/static/img/admin_portrait.jpg">
                            <!--                            <span>小羊</span>-->
                        </div>
                    </template>
                </bubble_text>
                <list
                        :need_border_top="false"
                        :list="posts.results">
                    <template v-slot:item-content="data">
                        <common_post_item
                                :post="data.item">
                        </common_post_item>
                    </template>
                </list>
                <div v-show="loading" class="loading">
                    <hexagon_loading></hexagon_loading>
                </div>
            </div>
            <div class="right">
                <sidebar_list
                        :list="hot"
                        title="热门推荐">
                    <template v-slot:item-content="data">
                        <svg class="icon-min" aria-hidden="true">
                            <use xlink:href="#icon-huo"></use>
                        </svg>
                        {{ data.item.name }}
                    </template>
                </sidebar_list>

                <div class="newest">

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState} from 'vuex'

    import {
        api_banner,
        api_post,
        api_hot
    } from '../../../api'
    import bubble_text from "../../../components/common/bubble_text"
    import sidebar_list from '../../../components/list/sidebar-list'
    import list from '../../../components/list/list'
    import common_post_item from '../../../components/list/item/common_post_item'
    import hexagon_loading from '../../../components/common/hexagon_loading'


    export default {
        name: "index",
        data() {
            return {
                input: '',
                banner: [],
                hot: [],
                posts: [],
                // tab栏目category选中状态
                one_category: 0,
                params: {
                    category: null,
                },
                disabled_scroll: false,
                loading: false,
                form: {
                    keyword: ''
                },
                isFixed: false,
                offsetTop: 0
            }
        },
        async asyncData(context) {
            let post_query = {
                category: context.query.category ? Number(context.query.category) : 0,
                offset: 0,
                limit: 10,
            }
            try {
                let banner, hot, posts
                let res = {
                    'banner': [],
                    'hot': [],
                    'posts': [],
                    'params': post_query,
                    // tab_category由二级分类传递到query,用于跳转时页面能获取到一级分类的选中状态
                    'one_category': Number(context.query.one_category) || post_query.category
                }
                let async_list = [
                    api_hot.list(),
                    api_post.list(post_query)
                ]
                if (post_query.category === 0) {
                    async_list.unshift(api_banner.list());
                    [banner, hot, posts] = await Promise.all(async_list)
                    res.banner = banner.data.data
                } else {
                    [hot, posts] = await Promise.all(async_list)
                }
                res.hot = hot.data.data
                res.posts = posts.data.data
                return res
            } catch (e) {
                context.error({statusCode: 500, message: 'ssr internal server error'})
            }
        },
        inject: ['generate_url', 'blank_push'],
        methods: {
            search() {
                return this.blank_push({name: 'search', query: this.form})
            },
            initHeight() {
                // 文章顶部栏吸顶效果
                var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
                this.isFixed = scrollTop - 15 > this.offsetTop ? true : false
                let el = document.getElementById('boxFixed')
                if (!el) return null
                if (this.isFixed) {
                    let width = document.getElementsByClassName('top')[0].clientWidth
                    el.style.width = `${width}px`
                } else {
                    el.style.width = 'initial'
                }
            },
            async _get_next_posts() {
                this.disabled_scroll = true
                if (isNaN(this.params.offset) || (this.params.offset >= this.posts.count)) {
                    return null
                }
                this.loading = true
                this.params.offset += this.params.limit
                let res = await api_post.list(this.params)
                res = res.data
                if (res.code === 2000) {
                    this.posts.results.push.apply(this.posts.results, res.data.results)
                } else {
                    this.params.offset -= this.params.limit
                    this.$message(res.msg)
                }
                this.loading = this.disabled_scroll = false
            },
        },
        computed: {
            ...mapState(['option']),
            two_categories() {
                for (let c of this.option.post_category) {
                    if (c.id === this.one_category) {
                        return c.child
                    }
                }
                return []
            }
        },
        beforeMount() {
            window.addEventListener('scroll', this.initHeight)
            this.$nextTick(() => {
                this.offsetTop = document.querySelector('#boxFixed').offsetTop
            })
        },
        destroyed() {
            window.removeEventListener('scroll', this.handleScroll)
        },
        components: {
            sidebar_list,
            list,
            common_post_item,
            hexagon_loading,
            bubble_text
        }
    }
</script>

<style scoped lang="scss">
    /* 提示图标 */
    .dialog_reply {
        img {
            display: block;
        }

        span {
            font-size: 12px;
        }
    }


    /* 吸顶 */
    .is_fixed {
        position: fixed;
        top: 0;
        z-index: 999;
        margin: 0;
        padding: 0 !important;
    }

    .loading {
        position: relative;
        height: 300px;
        width: 100%;
        zoom: .2;
    }

    .banner-wrap {
        position: relative;
        height: 100%;
        display: block;

        .banner-image {
            width: 100%;
            height: 100%;
            border-radius: 25px;
            object-fit: cover;
        }

        .banner-text {
            position: absolute;
            bottom: 0;
            left: 0;
            padding: 30px 0 12px 15px;
            font-family: PingFangSC-Medium;
            font-weight: 500;
            font-size: 18px;
            color: #fff;
            width: 100%;
            text-align: left;
            background: url('/img/banner_layer.png') no-repeat
        }
    }

    .el-carousel__item--card.is-in-stage {
        max-width: 580px;
        min-width: 35vw;
    }


    .top {
        width: 100%;

        .search-btn {
            height: 100%;
            display: flex;
        }

        .menuList {
            /*width: 800px;*/
            /*height: 60px;*/
            background-color: white;
            padding-bottom: 10px;

            .active {
                border-bottom: 2px solid #364045;
                /*background: #F0F0F5;*/
                a {
                    color: black;
                }
            }

            ul {
                /*width: 100%;*/
                height: 100%;
                display: flex;
                list-style: none;
                padding: 0;
                margin: 0;
                font-size: 16px;
                line-height: 45px;
                border-bottom: 1px solid #e4e7ed;

                li {
                    /*flex: 0 0 100px;*/
                    text-align: center;
                    cursor: pointer;
                    transition: 0.25s;

                    a {
                        padding: 0 20px;
                        display: block;
                        height: 100%;
                        color: #717181;
                    }
                }

                li:hover {
                    background: #F0F0F5;
                }
            }
        }
    }

    .content {
        text-align: initial;
        font-size: 0;

        .left {
            .el-tag {
                margin-right: 10px;
                transition: .25s;
            }

            .el-tag:hover {
                /*background: #364050;*/
                /*color: #F0F0F5;*/

                box-shadow: 0 0 2px 2px #BC8F8F
            }

            .el-tag-active {
                /*border-bottom: 1px solid black;*/
                /*background: #364050;*/
                /*color: #F0F0F5;*/
                /*color: black;*/

                color: #F0F0F5;
                background: #808080;
                /*border-bottom: 1px solid black;*/
            }

            font-size: 14px;
            width: 80%;
            display: inline-block;
            /*background: gold;*/
            vertical-align: top;
        }

        .right {
            width: 20%;
            font-size: 14px;
            display: inline-block;
            padding-left: 10px;

            .hot {
                .hot-title {
                    display: -webkit-box;
                    display: -ms-flexbox;
                    display: flex;
                    -webkit-box-align: center;
                    -ms-flex-align: center;
                    align-items: center;
                    font-size: 16px;
                    color: #4a4a4a;
                    height: 24px;
                    line-height: 24px;
                    margin-bottom: 5px;
                    position: relative;

                    .line {
                        display: block;
                        float: left;
                        width: 3px;
                        height: 16px;
                        background: #cf2730;
                        overflow: hidden;
                        margin-right: 5px;
                    }

                    .txt {
                        display: block;
                        float: left;
                        font-size: 16px;
                        color: #2c3033;
                    }
                }

                .sidebar-list-item {
                    margin-bottom: 10px;
                    height: 48px;
                    display: block;
                    border-bottom: 1px solid #e4e7ed;

                    .img-box {
                        float: left;
                        margin-right: 10px;
                        position: relative;

                        img {
                            cursor: pointer;
                            position: relative;
                            /*display: inline-block;*/
                            display: block;
                            width: 64px;
                            height: 48px;
                            border-radius: 3px;
                            vertical-align: top;
                            -o-object-fit: cover;
                            object-fit: cover;
                        }
                    }

                    .content {
                        padding-top: 2px;

                        .company_name {
                            display: block;
                            margin-bottom: 3px;
                            font-size: 12px;
                            color: #3d3d3d;
                            letter-spacing: 0;
                            line-height: 22px;
                            max-width: 200px;
                            overflow: hidden;
                            cursor: pointer;
                            font-weight: bold;
                            text-overflow: -o-ellipsis-lastline;
                            text-overflow: ellipsis;
                            display: -webkit-box;
                            -webkit-line-clamp: 2;
                            line-clamp: 2;
                            -webkit-box-orient: vertical;
                        }
                    }
                }
            }
        }

    }
</style>
