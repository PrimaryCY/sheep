import {
  RECEIVE_USERINFO,
  RECEIVE_OPTION
} from "./mutations-types"

import {
  get_user,
  delete_login,
  get_option
} from "../api/index"


export default {

  async receive_userinfo({commit},callback){
    //获取存储用户信息
    console.log('receive_userinfo')
    let user=await get_user()
    if(user.code===2000){
      let user_info=user.data
      commit(RECEIVE_USERINFO,user_info)
    }
    callback && callback()
  },
  async modify_userinfo({commit},data){
    //修改本地用户信息
    commit(RECEIVE_USERINFO,data)
  },
  async clear_userinfo({commit}) {
    //删除用户信息
    let user = await delete_login()
    console.log('delete_userinfo')
    if (user.code === 2000) {
      this._vm.$cookies.remove('tk')
      let user_info = {}
      commit(RECEIVE_USERINFO, user_info)
    }else {
      this._vm.$message(user.msg);
    }
  },
  async receive_option({commit},callback){
    console.log('receive_option')
    let res = await get_option()
    if(res.code===2000){
      commit(RECEIVE_OPTION,res.data)
    }else {
      this._vm.$message(res.msg)
    }
    callback && callback()
  }
}
