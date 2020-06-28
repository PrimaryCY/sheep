//全局配置文件
import Vue from 'vue'

let settings={
}

settings.DEBUG=true

if(settings.DEBUG){
  //socket的url地址
  settings.SOCKET_URL='http://127.0.0.1:5000'
  //后台url地址
  settings.SERVER_URL='http://127.0.0.1:8000/api'
}else {
  settings.SERVER_URL='http://192.168.3.5:8000/api'
  settings.SOCKET_URL='http://192.168.105.228:5000'
}


settings.TOKEN_NAME='tk'
settings.TOKEN_EXPIRE="7d"

settings.DEFAULT_PORTRAIT='https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png'

settings.REMEMBER_ME_EXPIRE='7d'


Vue.prototype.$settings = settings

export default settings