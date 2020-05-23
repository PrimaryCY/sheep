import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/store'

import settings from './conf/settings'
import VueCookies from 'vue-cookies';
Vue.prototype.$settings=settings
Vue.use(VueCookies)

if(settings.DEBUG){
  Vue.config.productionTip = true
}else {
  Vue.config.productionTip = false
}

// 导入静态文件
import '../public/static/css/reset.css';

//导入17素材的css文件
import '../public/static/css/5grid/core.css'
import '../public/static/css/style.css'
import '../public/static/css/5grid/core-desktop.css'
import '../public/static/css/style-desktop.css'
import '../public/static/css/5grid/core-1200px.css'
import '../public/static/css/style-1200px.css'

import './plugins/element/element'
import './plugins/vue-particles'
// import './plugins/mavon-editor'


import './utils/util'

export default new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
