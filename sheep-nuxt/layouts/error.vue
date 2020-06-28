<template>
  <div :style="{backgroundImage:statusCode===404?'url(\'/img/404.jpg\')':'url(\'/img/500.jpg\')'}">
    <button>123231</button>
  </div>
</template>

<script>
  export default {
    props: {
      error: {
        type: Object,
        default: null
      }
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
    }
  }
</script>

<style lang="scss" scoped>

  div{
    position: absolute;
    height: 100%; width: 100%;
    background-image: url('/img/404.jpg');
    background-repeat: no-repeat;
    background-size: 100% 100%;
  }
</style>
