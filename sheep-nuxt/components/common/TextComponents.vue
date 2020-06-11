<template>
  <div class="text-box" :class="textCard?'text-boxCard':''" :style="useInput?'align-items: center;':''">
    <span class="title" :style="`min-width:${titleWidth}%;`">
         <span v-if="title">{{title}}</span>
         <slot v-else name="iconfont"></slot>
        </span>
    <span v-if="!useInput" class="content" :style="`text-align:${contentAlign}`">{{content}}</span>
    <slot v-else name="input"></slot>
  </div>
</template>

<script>
  export default {
    props: {
      title: String, //左侧标题
      titleWidth: Number, //title的默认最小宽度，默认为20%
      content: String, //右侧内容
      contentAlign: String, //右侧内容文字方向 left/right/center，默认为 left
      textCard: Boolean, //是否显示为卡片效果，默认为false
      useInput: {default: false}, //是否显示input输入框
    },
  };
</script>

<style lang="scss" scoped>
  .text-box {
    width: 100%;
    display: flex;
    box-sizing: border-box;
    padding: 1rem;
    background: #f5f4f4;
    font-size: 0.88rem;
    margin: 0 auto;
    color: #808080;

    .title {
      display: inline-block;
      margin-right: 0.5rem;
      font-weight: bold;
      min-width: 10%;
      text-align: left;
    }
    .content {
      display: inline-block;
      width: 100%;
      text-align: left;
    }
    i{
      font-size: 1.5rem;
    }
    input{
      display: inline-block;
      width: 100%;
      height: 2rem;
      border: none;
      border-bottom: 1px solid goldenrod;
      background: transparent;
    }
  }
  .text-boxCard {
    margin: 1rem auto;
    width: 95%;
    box-shadow: 0rem 0.13rem 0.5rem 0rem rgba(235, 235, 235, 1);
    border-right: 0.5rem;
    background: white;
  }
</style>
