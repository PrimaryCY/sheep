<template>
    <div id="app" class="mobileUI-main-content">
        <!-- Wrapper -->
        <div id="wrapper" :class="{'pack-up':this.pack_up}">

            <!-- Content -->
            <div id="content" class="mobile-main-content">
                <router-view id="content-inner"></router-view>
            </div>

            <div class="sidebar">
                <!--pack-up-button-->
                <div class="pack-up-btn">
                    <el-switch
                            v-model="pack_up"
                            :width="20"
                            active-color="#7d7d83"
                            inactive-color="#b53c57">
                    </el-switch>
                </div>


                <div v-if="user.is_anonymity">
                    <!-- Logo -->
                    <div id="logo">
                        <el-button
                                type="danger"
                                :loading="loginBtn.loading"
                                class="login-btn"
                                @click.prevent="login"
                        >{{ loginBtn.loading ? '登陆中...' : '登录' }}
                        </el-button>
                    </div>
                    <!-- Nav -->
                    <nav id="nav" class="mobileUI-site-nav">
                        <ul>
                            <li :class="{current_page_item:active==='index'}" @click.prevent="push('/index')"><a
                                    href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-shiyongwendang"></use>
                                </svg>
                                首页
                            </a></li>
                            <li :class="{current_page_item:active==='feedback'}" @click.prevent="push('/feedback')"><a
                                    href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-yijianfankui"></use>
                                </svg>
                                意见反馈
                            </a></li>
                        </ul>
                    </nav>
                </div>
                <div v-else>
                    <!-- logo -->
                    <div class="user pointer" @click="push('/info',2)">
                        <el-avatar :size="60" :src="user.portrait">
                            <img :src="user.portrait"/>
                        </el-avatar>
                        <p class="username">
                            <svg v-if="user.gender===0" class="icon-min" aria-hidden="true">
                                <use xlink:href="#icon-xingbienv"></use>
                            </svg>
                            <svg v-else class="icon-min" aria-hidden="true">
                                <use xlink:href="#icon-xingbienan"></use>
                            </svg>
                            <b>{{ user.username }}</b>
                        </p>
                    </div>


                    <!--postings-->
                    <section class="is-search postings">
                        <div id="postings">
                            <el-button
                                    type="danger"
                                    class="login-btn"
                                    @click.prevent="blank_push('/postings')"
                            >
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-fabu"></use>
                                </svg>
                                发布/提问
                            </el-button>
                        </div>
                    </section>

                    <!--Nav-->
                    <nav id="nav" class="mobileUI-site-nav">
                        <ul>
                            <li :class="{current_page_item:active==='index'}" @click.prevent="push('/index')"><a
                                    href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-shiyongwendang"></use>
                                </svg>
                                首页
                            </a></li>
                            <li :class="{current_page_item:active==='my_post'}" @click.prevent="push('/my_post')"><a
                                    href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-chuangzuo"></use>
                                </svg>
                                我的文章
                            </a></li>
                            <li :class="{current_page_item:active==='my_question'}"
                                @click.prevent="push('/my_question')"><a href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-wenti--copy"></use>
                                </svg>
                                我的提问
                            </a></li>
                            <li :class="{current_page_item:active==='info'}" @click.prevent="push('/info')"><a href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-icon_zhanghao"></use>
                                </svg>
                                个人中心
                            </a></li>
                            <li :class="{current_page_item:['my_collect', 'my_collect_detail'].includes(active)}"
                                @click.prevent="push('/my-collect')"><a href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-sidebar-shoucang-copy"></use>
                                </svg>
                                我的收藏
                            </a></li>
                            <li :class="{current_page_item:active==='my_praise'}"
                                @click.prevent="push('/my-praise')"><a href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-icon_likegood"></use>
                                </svg>
                                我的点赞
                            </a></li>
                            <li :class="{current_page_item:active==='my_reply'}"
                                @click.prevent="push('/my-reply')"><a href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-icon_community_line"></use>
                                </svg>
                                消息回复
                            </a></li>
                            <li :class="{current_page_item:active==='my_history'}"
                                @click.prevent="push('/my-history')"><a href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-bofangjilu"></use>
                                </svg>
                                我的浏览
                            </a></li>
                            <li :class="{current_page_item:active==='feedback'}" @click.prevent="push('/feedback')"><a
                                    href="#">
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-yijianfankui"></use>
                                </svg>
                                意见反馈
                            </a></li>
                        </ul>
                    </nav>
                    <!--quit-->
                    <section class="is-text-style1">
                        <div class="inner" @click="quit()">
                            <p>
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-switch"></use>
                                </svg>
                                <span>退出</span>
                            </p>
                        </div>
                    </section>

                </div>

                <div>

                </div>
                <!-- Recent Posts -->
                <!--                <section class="is-recent-posts">-->
                <!--                    <header>-->
                <!--                        <h2>Recent Posts</h2>-->
                <!--                    </header>-->
                <!--                    <ul>-->
                <!--                        <li><a href="#">Nothing happened</a></li>-->
                <!--                        <li><a href="#">My Dearest Cthulhu</a></li>-->
                <!--                        <li><a href="#">The Meme Meme</a></li>-->
                <!--                        <li><a href="#">Now Full Cyborg</a></li>-->
                <!--                        <li><a href="#">Temporal Flux</a></li>-->
                <!--                    </ul>-->
                <!--                </section>-->

                <!-- Recent Comments -->
                <section class="is-recent-comments">
                    <header>
                        <h2>关于本站</h2>
                    </header>
                    <ul>
<!--                        <li @click="push('/about')" :class="{select:active==='about'}"><a href="#">关于我们</a>-->
<!--                        </li>-->
                        <li ><a href="/about" target="_blank">关于我们</a></li>
<!--                        <li><a href="#" target="_blank">广告服务</a></li>-->
                        <li><a href="#" target="_blank">我的愿景</a></li>
                        <li><a href="#">技术支持</a></li>
                        <li><a href="https://github.com/PrimaryCY/sheep" target="_blank">github 地址</a></li>
                        <li><a href="http://beian.miit.gov.cn" target="_blank">京ICP备2020034225号</a></li>
                    </ul>
                </section>

                <!-- Copyright -->
                <div id="copyright">
                    <p>
                        &copy; 2020 A personal Site.
                    </p>
                </div>

            </div>

        </div>

    </div>
</template>

<script>
import {mapState} from 'vuex'


export default {
    name: "index",
    inject: ['push', 'blank_push'],
    data() {
        return {
            loginBtn: {
                loading: false,
            },
        }
    },
    created() {
        this.$store.dispatch('modify_pack_up', this.$cookies.secure_get('pack_up'))
    },
    computed: {
        ...mapState(['user']),
        pack_up: {
            get() {
                return this.$store.state.pack_up
            },
            set(new_val) {
                this.$store.dispatch('modify_pack_up', new_val)
            }
        },
        active() {
            return this.$route.name
        },
    },
    methods: {
        async login() {
            console.log('login')
            this.loginBtn.loading = true
            this.$router.push('/login')
            this.loginBtn.loading = false
        },
        async quit() {
            // 退出登录
            let res = await this.$confirm('此操作将退出登录?', '退出登录', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
                roundButton: true,
                customClass: 'message'
            }).catch(() => {
            })
            if (res === 'confirm') {
                await this.$store.dispatch('clear_userinfo')
                await this.$store.dispatch('receive_userinfo')
                this.$router.push({name: 'index'})
            }
        }
    },
}
</script>

<style scoped lang="scss">
/*
.select {
    a {
        font-weight: 800;
        color: #fff;
    }
}
 */

@media (min-width: 1200px) {
    .pack-up {
        .sidebar {
            width: 70px;
            padding: 1.5em 1em 1em 1em;

            .pack-up-btn {
                /*text-align: center;*/
            }

            /*登录按钮*/
            #logo {
                margin: 0;

                button {
                    white-space: initial;
                    overflow: hidden;
                    padding: 0;
                    font-size: 13px;
                }
            }

            /*发表文章按钮*/
            #postings {
                margin: 0;

                button {
                    white-space: pre;
                    letter-spacing: 18px;
                    overflow: hidden;
                    padding: 37%;
                }

            }

            /*用户信息*/
            .user {
                span {
                    height: 47px !important;
                    width: 47px !important;
                }

                .username {
                    display: none;
                }
            }

            /*搜索框*/
            section:nth-child(2) {
                display: none;
            }

            /*功能列表*/
            section, nav {
                margin: 1.5em 0 0 0;
                overflow: hidden;

                li a {
                    height: 30px;
                    overflow: hidden;
                    word-wrap: break-word;
                    word-break: normal;
                    /*letter-spacing: 3px;*/
                }
            }

            /*退出按钮*/
            .is-text-style1 .inner {
                overflow: hidden;

                p {
                    height: 34px;
                    overflow: hidden;

                    svg {
                        margin: 10px
                    }
                }
            }
        }

        #content {
            margin-left: 8% !important;
            min-height: 118em;

            #content-inner {
                max-width: 95%;
            }
        }
    }
}

.pack-up-btn {
    margin-bottom: 15px;
    text-align: right;
    width: 100%;
    -webkit-transform: scale(.8, .8) !important;
    /*-webkit-transform-origin: 0 0!important;*/
}

.user {
    .username {
        padding-top: 2%;
        word-break: break-all;

        b {
            color: white;
        }
    }
}

/*去掉火狐动画效果*/
@-moz-document url-prefix() {
    #content {
        transition: none !important;
    }
    .sidebar {
        transition: none !important;
    }
}

#content {
    min-height: 103em;
    /* 去除动画,动画卡顿*/
    /*transition: margin-left 0.25s ease-in-out;*/
}

.sidebar {
    /* 去除动画,动画卡顿*/
    /*transition: width 0.25s ease-in-out;*/
    -moz-box-shadow: 7px 0px 15px #595654;
    -webkit-box-shadow: 7px 0px 15px #595654;
    box-shadow: 7px 0px 15px #595654;
    border-top-right-radius: 1%;
    border-bottom-right-radius: 1%;
}


#logo {
    padding: 0;
    margin: 10px;

    .login-btn {
        background-color: #c94663;
        width: 100%;
        height: 70px;
        border: 0;
        font-size: 18px;
        margin: 0;
        padding: 0;
    }

    .login-btn:active {
        background-color: #a14663;
    }
}

#postings {
    padding: 0;
    margin: 10px;

    .login-btn {
        background-color: #b53c57;
        width: 100%;
        height: 50px;
        border: 0;
        font-size: 12px;
        margin: 0;
    }

    .login-btn:active {
        background-color: #a14663;
    }
}

</style>
