<template>
  <div :style="{backgroundImage:statusCode===404?'url(\'/img/404.jpg\')':'url(\'/img/500.jpg\')'}">
    <button class="noselect not_found">
      返回首页
      <span> &gt;&gt;&gt;</span>
    </button>
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
  .not_found{
    position: absolute;
    bottom: 45%;
    right: 25%;
    border: 2px solid cornflowerblue;
    color: cadetblue;
  }
  .not_found:hover span{
    color: cadetblue!important;
  }

  button {
    font-family: 'Play', sans-serif;
    font-size: 16px;
    background: transparent;
    border: 2px solid #eee;
    width: 150px;
    height: 50px;
    border-radius: 5px;
    color: #eee;
    -webkit-tap-highlight-color: transparent;
    cursor: pointer;
    transition: 400ms ease-in-out;
    margin: 0 10px 0 10px;
  }

  .noselect {
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }

  button:hover {
    width: 170px;
    background: #777;
    border: 2px solid #777;
    margin: 0;
  }

  button:focus {
    border: none;
  }

  button span {
    color: transparent;
    transition: 500ms;
    margin-left: -20px;
  }

  button:hover span {
    color: #d3d3d3;
    margin-left: 0;
  }
  div{
    position: absolute;
    height: 100%; width: 100%;
    background-image: url('/img/404.jpg');
    background-repeat: no-repeat;
    background-size: 100% 100%;
  }
</style>
