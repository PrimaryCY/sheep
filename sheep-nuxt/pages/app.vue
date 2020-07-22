<template>
  <div>
    <!--  系统页面升级  -->
    <upgrade v-if="upgrade"></upgrade>
    <div v-else>
      <!-- 用于页面刷新 -->
      <nuxt v-if="isRouterAlive"></nuxt>
    </div>
    <backtop v-show="!$route.no_back_top"></backtop>
  </div>
</template>

<script>
  import {mapState} from 'vuex'

  import backtop from '../components/backtop'
  import upgrade from '@/components/common/upgrade'
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
        upgrade:false
      }
    },
    async asyncData(context){
      try {
        if(context.app.$cookies.secure_get(setting.TOKEN_NAME)
          && !context.store.user){
          await context.store.dispatch('receive_userinfo')
        }
      }catch(e)
      {
       context.error({statusCode:500,message:'ssr internal server error'})
      }

      let word_list = []
      // 远程获取公共配置
      if(!context.store.state.option.post_category){
        word_list.push(context.store.dispatch('receive_option'))
      }
      await Promise.all(word_list).catch(
        ()=>{
          context.error({statusCode:500,message:'ssr internal server error'})
        }
      )
    },
    components:{
      backtop,
      upgrade
    },
    computed:{
      ...mapState(['user','option'])
    }
  }
</script>
<style scoped>

</style>
