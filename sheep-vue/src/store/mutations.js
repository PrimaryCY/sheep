import {
  RECEIVE_USERINFO,
} from './mutations-types'

export default {
  //保存用户信息
  [RECEIVE_USERINFO](state,user){
    state.user=user
  },
}
