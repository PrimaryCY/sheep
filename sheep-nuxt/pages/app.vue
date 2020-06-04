<template>
  <div>
    <nuxt></nuxt>

    <backtop v-show="!$route.no_back_top"></backtop>
  </div>
</template>

<script>
  import {mapState} from 'vuex'

  import backtop from '../components/backtop'
  import setting from '../conf/settings'
  import browser_mixin from '../mixins/browser_mixin'
  import '../plugins/util'

  export default {
    name: 'app',
    mixins:[
      browser_mixin
    ],
    data () {
      return {
        isRouterAlive: true,
      }
    },
    async asyncData(context){
      let word_list = []
      if(context.app.$cookies.secure_get(setting.TOKEN_NAME)
        && !context.store.user){
        word_list.push(context.store.dispatch('receive_userinfo'))
      }
      // 远程获取公共配置
      if(!context.store.option){
        word_list.push(context.store.dispatch('receive_option'))
      }
      await Promise.all(word_list)
    },
    components:{
      backtop,
    },
    computed:{
      ...mapState(['user','option'])
    }
  }
</script>
<style scoped>

</style>
