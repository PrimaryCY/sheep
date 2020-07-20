import {
  RECEIVE_USERINFO,
  RECEIVE_OPTION,
  MODIFY_PACK_UP
} from './mutations-types'

export default {
  //保存用户信息
  [RECEIVE_USERINFO](state,user){
    state.user=user
  },
  //保存远端公共配置
  [RECEIVE_OPTION](state,option){
    state.option=option
  },
  // 修改侧边栏状态值
  [MODIFY_PACK_UP](state, pack_up){
    state.pack_up=pack_up
  }
}
