import {Message} from 'element-ui'

import settings from '@/conf/settings'
import axios from 'axios'

let NProgress = require('nprogress')
if(process.server){
  NProgress = {
    start:()=>{},
    done:()=>{}
  }
}
let service=axios.create({
  baseURL:settings.SERVER_URL,
  timeout:9000,
  headers:{
    'content-type':'application/json',//转换为key=value的格式必须增加content-type
  },
})


export default function (context) {

  context.$axios = service
  service.interceptors.request.use(
    request => {
      NProgress.start()
      if (context.app.$cookies.get(settings.TOKEN_NAME)) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
        request.headers.tk = context.app.$cookies.secure_get(settings.TOKEN_NAME);
      }
      return request;
    },
    err => {
      return Promise.reject(err);
    });

//http-响应拦截
  service.interceptors.response.use(
    function (response){
      console.log(response.data)
      switch(response.data.code) {
        case 4101||4104||4105:
          context.app.$cookies.remove(settings.TOKEN_NAME)
          console.log('用户令牌失效或无权限!')
          context.redirect('/login')
          // Message(response.data.msg)
          break
      }
      NProgress.done()
      return response;
    },
    error => {
      if(!error.response){
        Message('网络连接错误,请检查网络!')
      }else {
        switch (error.response.status) {
          case 404:
            Message('网络错误:'+error.response.status)
            break
          case 500:
            Message('500 internal server error');
            break
        }
      }
      return Promise.reject(error)
    }
  )
}

export {service}
