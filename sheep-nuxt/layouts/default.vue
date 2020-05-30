<template>
  <nuxt></nuxt>
</template>



<style >
  body{
    /*仿chrome缩放*/
    /*-webkit-transform: scale(.8,.8) !important;*/
    /*-webkit-transform-origin: 0 0!important;*/
  }
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }


  [v-cloak] {
    display: none;
  }

  /*修改顶部加载条颜色*/
  #nprogress .bar {
    background: #b53c57 !important;
  }

  /*修改element的默认样式*/
  .el-message-box__wrapper .message{
    width: 300px!important;
  }
  .el-button--mini{
    padding: 5px 11px!important;
    font-size: 10px!important;
  }


</style>
