<template>
  <div class="base">
    <div class="notice-wrap">
      <div class="notice">
        <h1>系统升级通知</h1>
        <p class="notice-cont">尊敬的访客您好<span>Sheep</span>后台正在进行升级</p>
        <p class="notice-tel">请您稍后访问 或联系腾互联<span>此次攻击 祁风互联已经开通的服务不受影响</span>感谢您对Sheep的支持</p>
        <div class="notice-foot">
          <p>腾互联</p>
<!--          <p>错误代码：404</p>-->
        </div>
        <audio autoplay>
          <source src="https://music.163.com/song/media/outer/url?id=1388407065.mp3" type="audio/mpeg"><!-- ！BGM！-->
        </audio>
      </div>
    </div>
  </div>

</template>

<script>
  export default {
    name: 'upgrade'
  }
</script>

<style scoped lang="scss">
  .base{
    width: 100%;
    height: 100%;
    background: #ff6500;
    position: absolute;
    font-family: "微软雅黑";
  }
  .notice-wrap{
    padding-top: 20px;
  }
  .notice{
    margin: 0 auto;
    width: 552px;
    height: 503px;
    background: url('../../static/img/update-bg.png') no-repeat;
    border-radius: 10%;
    background-size: 100%;
  }
  .notice h1{
    padding-top: 195px;
    font-size: 30px;
    color: #333;
    text-align: center;
  }
  .notice>p{
    margin: 0 52px;
    font-size: 12px;
    color: #666;
    text-indent: 32px;
    line-height: 36px;
  }
  p span{
    color: #ff6500;
  }
  .notice .notice-cont{
    margin-top: 30px;
  }
  .notice .notice-tel{
    padding-bottom: 35px;
    border-bottom: 2px solid #f2f2f2;
  }
  .notice-foot{
    margin-top: 24px;
  }
  .notice-foot p{
    font-size: 14px;
    color: #666;
    text-align: center;}
</style>
