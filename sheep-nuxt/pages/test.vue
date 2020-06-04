<template>
  <div>
    <p>123</p>
  </div>
</template>

<script>
  import {mapState} from 'vuex'

  import '../plugins/util'
  import {api_user, api_option} from '../api'

  export default {
    name: 'app',
    data () {
      return {
      }
    },
    methods: {
    },
    async asyncData(context){
      // let url = '/v1/web/user/'
      // await context.$axios(
      //   {
      //     methods:'get',
      //     url
      //   }
      // )
      // await context.app.$axios(
      //   {
      //     methods:'get',
      //     url:'/v1/option/'
      //   }
      // )
      let res = await Promise.all([api_user.list(),api_option.list()])
      for (let r of  res){
        console.log(r.data)
      }
    },
    components:{
    },
    computed:{
      ...mapState(['user','option'])
    }
  }
</script>
<style scoped>

</style>
