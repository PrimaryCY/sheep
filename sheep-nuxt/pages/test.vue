<template>
<!--  <img style="width:100%;height:100%" src="~/Images/chatBack.jpg">-->
  <div class="container">
    <div>头像</div>
    <div class="talk-bubble tri-right round right-in">
      <div class="talktext">
        <p>
          Moving our way back up the right side indented. Uses .round and .right-in
          Moving our way back up the right side indented. Uses .round and .right-in
          Moving our way back up the right side indented. Uses .round and .right-in
          Moving our way back up the right side indented. Uses .round and .right-in
          Moving our way back up the right side indented. Uses .round and .right-in
          Moving our way back up the right side indented. Uses .round and .right-in
          Moving our way back up the right side indented. Uses .round and .right-in
          Moving our way back up the right side indented. Uses .round and .right-in
          2132222222222222222222222222222222222222222
          2132222222222222222222222222222222222222222
          2132222222222222222222222222222222222222222
          2132222222222222222222222222222222222222222
          2132222222222222222222222222222222222222222
          2132222222222222222222222222222222222222222
          2132222222222222222222222222222222222222222
          2132222222222222222222222222222222222222222
        </p>
      </div>
    </div>
  </div>

</template>

<script>
  import {mapState} from 'vuex'

  import '../plugins/util'

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
      // let res = await Promise.all([api_user.list(),api_option.list()])
      // for (let r of  res){
      //   console.log(r.data)
      // }
    },
    components:{
    },
    computed:{
      ...mapState(['user','option'])
    }
  }
</script>
<style scoped lang="scss">
  /* container */
  .container {
    padding: 5% 5%;
  }

  /* CSS talk bubble */
  .talk-bubble {
    margin: 40px;
    display: inline-block;
    position: relative;
    width: 200px;
    height: auto;
    background-color: lightyellow;
  }
  .round{
    border-radius: 30px;
    -webkit-border-radius: 30px;
    -moz-border-radius: 30px;

  }

  /* Right triangle placed top left flush. */
  .tri-right.border.left-top:before {
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: -40px;
    right: auto;
    top: -8px;
    bottom: auto;
    border: 32px solid;
    border-color: #666 transparent transparent transparent;
  }
  .tri-right.left-top:after{
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: -20px;
    right: auto;
    top: 0px;
    bottom: auto;
    border: 22px solid;
    border-color: lightyellow transparent transparent transparent;
  }

  /* Right triangle, left side slightly down */
  .tri-right.border.left-in:before {
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: -40px;
    right: auto;
    top: 30px;
    bottom: auto;
    border: 20px solid;
    border-color: #666 #666 transparent transparent;
  }
  .tri-right.left-in:after{
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: -20px;
    right: auto;
    top: 38px;
    bottom: auto;
    border: 12px solid;
    border-color: lightyellow lightyellow transparent transparent;
  }

  /*Right triangle, placed bottom left side slightly in*/
  .tri-right.border.btm-left:before {
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: -8px;
    right: auto;
    top: auto;
    bottom: -40px;
    border: 32px solid;
    border-color: transparent transparent transparent #666;
  }
  .tri-right.btm-left:after{
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: 0px;
    right: auto;
    top: auto;
    bottom: -20px;
    border: 22px solid;
    border-color: transparent transparent transparent lightyellow;
  }

  /*Right triangle, placed bottom left side slightly in*/
  .tri-right.border.btm-left-in:before {
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: 30px;
    right: auto;
    top: auto;
    bottom: -40px;
    border: 20px solid;
    border-color: #666 transparent transparent #666;
  }
  .tri-right.btm-left-in:after{
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: 38px;
    right: auto;
    top: auto;
    bottom: -20px;
    border: 12px solid;
    border-color: lightyellow transparent transparent lightyellow;
  }

  /*Right triangle, placed bottom right side slightly in*/
  .tri-right.border.btm-right-in:before {
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: auto;
    right: 30px;
    bottom: -40px;
    border: 20px solid;
    border-color: #666 #666 transparent transparent;
  }
  .tri-right.btm-right-in:after{
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: auto;
    right: 38px;
    bottom: -20px;
    border: 12px solid;
    border-color: lightyellow lightyellow transparent transparent;
  }

	/*Right triangle, placed bottom right side slightly in*/
  .tri-right.border.btm-right:before {
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: auto;
    right: -8px;
    bottom: -40px;
    border: 20px solid;
    border-color: #666 #666 transparent transparent;
  }
  .tri-right.btm-right:after{
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: auto;
    right: 0px;
    bottom: -20px;
    border: 12px solid;
    border-color: lightyellow lightyellow transparent transparent;
  }

  /* Right triangle, right side slightly down*/
  .tri-right.border.right-in:before {
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: auto;
    right: -40px;
    top: 30px;
    bottom: auto;
    border: 20px solid;
    border-color: #666 transparent transparent #666;
  }
  .tri-right.right-in:after{
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: auto;
    right: -20px;
    top: 38px;
    bottom: auto;
    border: 12px solid;
    border-color: lightyellow transparent transparent lightyellow;
  }

  /* Right triangle placed top right flush. */
  .tri-right.border.right-top:before {
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: auto;
    right: -40px;
    top: -8px;
    bottom: auto;
    border: 32px solid;
    border-color: #666 transparent transparent transparent;
  }
  .tri-right.right-top:after{
    content: ' ';
    position: absolute;
    width: 0;
    height: 0;
    left: auto;
    right: -20px;
    top: 0px;
    bottom: auto;
    border: 20px solid;
    border-color: lightyellow transparent transparent transparent;
  }

  /* talk bubble contents */
  .talktext{
    padding: 1em;
    text-align: left;
    line-height: 1.5em;
  }
  .talktext p{
    /* remove webkit p margins */
    -webkit-margin-before: 0em;
    -webkit-margin-after: 0em;
  }
</style>
