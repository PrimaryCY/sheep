<template>
  <div>
    <nuxt v-if="isRouterAlive" ></nuxt>

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
    methods: {
      async _get_option(){
        // 远程获取公共配置
        if(process.client&&!this.option.post_category){
          await this.$store.dispatch('receive_option')
        }
      },
    },
    async asyncData(context){
      if(context.app.$cookies.secure_get(setting.TOKEN_NAME)
        && !context.store.user){
        await context.store.dispatch('receive_userinfo')
      }
    },
    async created(){
      // await this._get_user_info()
      await this._get_option()
    },
    components:{
      backtop
    },
    computed:{
      ...mapState(['user','option'])
    }
  }
</script>
<style scoped>

</style>
