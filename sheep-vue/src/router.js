import Vue from 'vue'
import VueRouter from 'vue-router'
import VueCookies from 'vue-cookies'

Vue.use(VueRouter)


// const index_vue=()=>import ('./views/index_vue/index_vue.vue')
// const index=()=>import('./views/index_vue/index/index.vue')
import index_vue from './views/index_vue/index_vue'
import login from './views/login/login'
import postings from './views/postings/postings'

import index from './views/index_vue/index/index'
import info from './views/index_vue/info/info'
import my_post from './views/index_vue/my_post/my_post'

import NotFound from './views/notFound/notFound'
import test from './views/test/test'

import setting from './conf/settings'


const routes = [
  // {
  //   path:'/',
  //   redirect:'/index_vue',
  // },

  // 首页模板
  {
    path: '',
    name: 'index_vue',
    component: index_vue,
    meta:{
      keepAlive:true
    },
    children:[
      {
        // 首页
        path:'index/',
        name:'index',
        component:index,
      },
      {
        // 个人信息
        path:'info/',
        name:'info',
        component:info,
        meta:{
          isLogin:true
        }
      },
      {
        // 我的文章
        path:'my_post',
        name:'my_post',
        component:my_post,
        meta:{
          isLogin:true
        }
      },
      {
        path:'',
        redirect:'index'
      }
    ]
  },
  {
    // 创建帖子
    path:'/postings',
    name:'postings',
    component:postings,
    meta:{
      // isLogin:true
    }
  },
  {
    path:'/login',
    name:'login',
    component: login
  },
  {
    path:'/test',
    name:'test',
    component: test
  },
  {
    path:'*',
    component:NotFound
  }
]


const router = new VueRouter({
  // mode: 'history',
  base: process.env.BASE_URL,
  routes
})


router.beforeEach((to, from, next) => {
  //如果未登录不可以访问修改用户资料的页面
  if(to.meta.isLogin){
    if(!VueCookies.get(setting.TOKEN_NAME)){
      next({
        path: '/login',
        query: {redirect: to.fullPath}   //登录成功后重定向到当前页面
      })
    }
  }
  // 删除全局zoom属性
  /*特定页面需要移除zoom属性,否则会造成页面弹窗,动画偏移*/
  if(['login'].includes(to.name)){
    let el = document.getElementsByTagName('body')[0]
    el.style.zoom='initial'
  }else {
    let el = document.getElementsByTagName('body')[0]
    el.style.zoom='.8'
  }
  next()
})


export default router
