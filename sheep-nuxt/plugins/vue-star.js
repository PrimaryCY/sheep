import Vue from 'vue'
if(process.client){
  let VueStar = require('vue-star')
  Vue.component('VueStar', VueStar)
}
