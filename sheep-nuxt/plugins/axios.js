import {Message} from 'element-ui'

import settings from '@/conf/settings'
import axios from 'axios'

import NProgress from 'nprogress'

let service = {}

export default function (context, inject) {
  service= axios.create({
    baseURL:settings.SERVER_URL,
    timeout:10000,
    // withCredentials: true,
    headers:{
      'content-type':'application/json',
    },
  })

  inject('axios', service)

  service.interceptors.request.use(
    request => {
      console.log('start request')
      if(process.client){
        NProgress.start()
      }
      if(process.server){
        // 为了解决ssr渲染后端还能查询到匿名用户,新增header:u-host
        request.headers['u-host'] = context.req.socket.remoteAddress
      }
      if (context.app.$cookies.get(settings.TOKEN_NAME)) {
        // 判断是否存在token，如果存在的话，则每个http header都加上token
        request.headers.tk = context.app.$cookies.secure_get(settings.TOKEN_NAME);
      }
      return request;
    },
    err => {
      return Promise.reject(err);
    });

  //http-响应拦截
  service.interceptors.response.use(
    function (response) {
      console.log(response.data.code)
      switch(response.data.code) {
        case 4101:
          context.app.$cookies.remove(settings.TOKEN_NAME)
          console.log('用户登录失效!')
          context.redirect('/login')
          break
        case 4105:
          console.log('用户无权限!')
          break
      }
      if(process.client) {
        NProgress.done()
      }
      return response;
    },
    error => {
      if (!error.response) {
        // console.log(error.response)
        Message('网络连接错误,请检查网络!')
      } else {
        switch (error.response.status) {
          case 404:
            Message('网络错误:' + error.response.status)
            break
          case 500:
            context.error({
              statusCode: error.response.status,
              message: '500 internal server error'
            })
            break
        }
      }
      return Promise.reject(error)
    }
  )
}

export {service}
