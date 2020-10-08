import Vue from 'vue'
import VueRouter from 'vue-router'
import settings from '@/conf/settings'

Vue.use(VueRouter)

import app from './pages/app'
import index_vue from './pages/index_vue/index_vue'
import login from './pages/login/login'
import postings from './pages/postings/postings'

import index from './pages/index_vue/index/index'
import info from './pages/index_vue/info/info'
import my_post from './pages/index_vue/my_post/my_post'
import my_question from './pages/index_vue/my_question/my_question'
import feedback from './pages/index_vue/feedback/feedback'
import not_found from './pages/index_vue/not_found/not_found'
import post_detail from './pages/index_vue/post_detail/post_detail'
import search from './pages/index_vue/search/search'
import my_collect from './pages/index_vue/my_collect/my_collect'
import my_collect_detail from './pages/index_vue/my_collect_detail/my_collect_detail'
import my_praise from './pages/index_vue/my_praise/my_praise'
import my_history from "./pages/index_vue/my_history/my_history"
import my_reply from "@/pages/index_vue/my_reply/my_reply"
import about from "@/pages/index_vue/about/about"

// import NotFound from './views/notFound/notFound'
// import test from './pages/test'

// import setting from './conf/settings'


const routes = [
    // {
    //   path:'/',
    //   redirect:'/index_vue',
    // },
    {
        path: '',
        component: app,
        children: [
            // 首页模板
            {
                path: '',
                component: index_vue,
                meta: {
                    keepAlive: true,
                },
                children: [
                    {
                        // 首页
                        path: 'index/',
                        name: 'index',
                        component: index,
                    },
                    {
                        // 个人信息
                        path: 'info/',
                        name: 'info',
                        component: info,
                        meta: {
                            is_login: true
                        }
                    },
                    {
                        // 我的文章
                        path: 'my_post',
                        name: 'my_post',
                        component: my_post,
                        meta: {
                            is_login: true
                        }
                    },
                    {
                        // 我的提问
                        path: 'my_question',
                        name: 'my_question',
                        component: my_question,
                        meta: {
                            is_login: true
                        }
                    },
                    {
                        path: 'my-reply',
                        name: 'my_reply',
                        component: my_reply,
                        meta: {
                            is_login: true
                        }
                    },
                    {
                        path: 'feedback',
                        name: 'feedback',
                        component: feedback,
                        meta: {}
                    },
                    {
                        path: 'search',
                        name: 'search',
                        component: search,
                        meta: {}
                    },
                    {
                        path: 'my-collect',
                        name: 'my_collect',
                        component: my_collect,
                        meta: {
                            is_login: true
                        }
                    },
                    {
                        path: 'my-collect/:id',
                        name: 'my_collect_detail',
                        component: my_collect_detail,
                        meta: {
                            is_login: true
                        }
                    },
                    {
                        path: 'post-detail/:id',
                        name: 'post_detail',
                        component: post_detail
                    },
                    {
                        path: 'my-praise',
                        name: 'my_praise',
                        component: my_praise,
                        meta: {
                            is_login: true
                        }
                    },
                    {
                        path: 'my-history',
                        name: 'my_history',
                        component: my_history,
                        meta: {
                            is_login: true
                        }
                    },
                    {
                        path: 'about',
                        name: 'about',
                        component: about
                    },
                    {
                        path: '',
                        redirect: 'index'
                    },
                    {
                        path: 'not-found/',
                        name: "not_found",
                        component: not_found
                    }
                ]
            },
            {
                // 创建帖子
                path: '/postings/',
                name: 'postings',
                component: postings,
                meta: {
                    no_back_top: true,
                    is_login: true
                }
            },
            {
                // 修改帖子
                path: '/postings/:id',
                name: 'postings_detail',
                component: postings,
                meta: {
                    no_back_top: true,
                    is_login: true
                }
            },
            {
                path: '/login',
                name: 'login',
                component: login,
                meta: {}
            },
            // {
            //   path:'*',
            //   component:NotFound
            // }
        ],
    },
    // {
    //     path: '/test',
    //     component: test
    // }
]

export function createRouter() {
    const router = new VueRouter({
        mode: 'history',
        // base: process.env.BASE_URL,
        routes
    })
    router.beforeEach((to, from, next) => {
        if (to.meta.is_login) {
            if (!process.$cookies.secure_get(settings.TOKEN_NAME)) {
                next({
                    path: '/login',
                    query: {redirect: to.fullPath}   //登录成功后重定向到当前页面
                })
            }
        }
        next()
    })
    return router
}




