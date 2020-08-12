import {
  RECEIVE_USERINFO,
  RECEIVE_OPTION,
  MODIFY_PACK_UP
} from "./mutations-types"

import {
  api_user,
  api_login,
  api_option
} from "../api/index"
import settings from '@/conf/settings'
import { Message } from 'element-ui'


export default {
  // nuxtServerInit({commit}, {app, req}) {
    // app.$cookies = req.$cookies
    // commit
    // let cookie = req.headers.cookie;
  // },
  async receive_userinfo({commit},callback){
    //获取存储用户信息
    console.log('receive_userinfo')
    let res=await api_user.list()
    // console.log(res)
    if(res.data.code===2000){
      let user_info=res.data.data
      commit(RECEIVE_USERINFO,user_info)
    }else {
      Message('用户登录失效!')
    }
    callback && callback(res)
  },
  async modify_userinfo({commit},data){
    //修改本地用户信息
    commit(RECEIVE_USERINFO,data)
  },
  async clear_userinfo({commit}) {
    //删除用户信息
    let user = await api_login.destory()
    console.log('delete_userinfo')
    user = user.data
    console.log(user)
    if (user.code === 2000) {
      process.$cookies.remove(settings.TOKEN_NAME)
      commit(RECEIVE_USERINFO, {})
    }
  },
  async receive_option({commit},callback){
    console.log('receive_option')
    let res = await api_option.list()
    if(res.data.code===2000){
      commit(RECEIVE_OPTION,res.data.data)
    }else {
      this._vm.$message(res.data.msg)
    }
    callback && callback()
  },
  modify_pack_up({commit}, data){
    // 点击收起时存入cookie中
    data = Boolean(data)
    commit(MODIFY_PACK_UP, data)
    process.$cookies.secure_set('pack_up', data, {maxAge:60*60*24*7})
  }
}
