<template>
  <!-- Right -->
  <div class="receiver">
    <div>
<!--      <img src="chatTemplateExample2_files/cat.jpg">-->
      <span>机器人</span>
    </div>
    <div>
      <div class="right_triangle"></div>
      <span> 感谢您的意见!我们正在修改中! </span>
    </div>
    <div style="clear: both"></div>
  </div>
</template>

<script>
  export default {
    name: 'bubble_text'
  }
</script>

<style scoped lang="scss">
  /* bubble style */
  .sender{
    clear:both;
  }
  .sender div:nth-of-type(1){
    float: left;
  }
  .sender div:nth-of-type(2){
    background-color: aquamarine;
    float: left;
    margin: 0 20px 10px 15px;
    padding: 10px 10px 10px 0px;
    border-radius:7px;
  }

  .receiver div:first-child img,
  .sender div:first-child img{
    width:50px;
    height: 50px;
  }

  .receiver{
    clear:both;
  }
  .receiver div:nth-child(1){
    float: right;
  }
  .receiver div:nth-of-type(2){
    float:right;
    background-color: #f7f4e5;
    margin: 0 10px 10px 20px;
    padding: 10px 0px 10px 10px;
    border-radius:7px;
  }

  .left_triangle{
    height:0px;
    width:0px;
    border-width:8px;
    border-style:solid;
    border-color:transparent aquamarine transparent transparent;
    position: relative;
    left:-16px;
    top:3px;
  }
  .right_triangle{
    height:0px;
    width:0px;
    border-width:8px;
    border-style:solid;
    border-color:transparent transparent transparent #f7f4e5;
    position: relative;
    right:-16px;
    top:3px;
  }
</style>
