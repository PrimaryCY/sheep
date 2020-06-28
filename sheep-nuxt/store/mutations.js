import {
  RECEIVE_USERINFO,
  RECEIVE_OPTION
} from './mutations-types'

export default {
  //保存用户信息
  [RECEIVE_USERINFO](state,user){
    state.user=user
  },
  //保存远端公共配置
  [RECEIVE_OPTION](state,option){
    state.option=option
  }
}
