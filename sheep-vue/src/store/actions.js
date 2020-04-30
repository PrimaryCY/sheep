import {
  RECEIVE_USERINFO,
} from "./mutations-types"

import {
  get_user,
  delete_login,
} from "../api/index"


export default {

  async receive_userinfo({commit},callback){
    //获取存储用户信息
    let user=await get_user()
    console.log('receive_userinfo')
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
}
