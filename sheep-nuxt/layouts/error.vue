<template>
  <div :style="{backgroundImage:statusCode===404?'url(\'/img/404.jpg\')':'url(\'/img/500.jpg\')'}">
    <div class="go_back">
      <h1 class="go_back_text">
        {{count_down}}秒后自动返回首页,<a href="/index">点击此处</a>立即返回首页
      </h1>
    </div>
  </div>
</template>

<script>
  export default {
    data(){
      return {
        count_down:3
      }
    },
    props: {
      error: {
        type: Object,
        default: null
      },
    },
    computed: {
      statusCode () {
        return (this.error && this.error.statusCode) || 500
      },
      message () {
        return this.error.message || 'Error'
      }
    },
    head () {
      return {
        title: `${this.statusCode === 404 ? '找不到页面' : '呈现页面出错'}`,
        meta: [
          {
            name: 'viewport',
            content: 'width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no'
          }
        ]
      }
    },
    methods: {
      _timed_task() {
        this.count_down --;
        if(this.count_down<=0&& this.count_down>=-2){
          return this.$router.replace('/index')
        }
        console.log(this.count_down);
      }
    },
    mounted() {
      this.timer = setInterval(this._timed_task, 1000);
    },
    beforeDestroy() {
      clearInterval(this.timer);
    }
  }
</script>

<style lang="scss" scoped>
  .go_back{
    position: absolute;
    top: 0;
    height: initial;
    width: 100%;
    text-align: center;
    background: rgba(244,68,68,0.9);
    .go_back_text{
      padding: 5px 0;
      color: #fff;
      a{
        color: #fff;
        text-decoration: underline;
        cursor: pointer;
      }
      a:hover{
        color: #c94663;
      }
    }
  }

  div{
    position: absolute;
    height: 100%; width: 100%;
    background-image: url('/img/404.jpg');
    background-repeat: no-repeat;
    background-size: 100% 100%;
  }
</style>
