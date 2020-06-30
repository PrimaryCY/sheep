import Vue from 'vue'


Vue.prototype.openLoading = function({text = '加载中',target = 'body',time_out = 5000}) {
  const loading = this.$loading({           // 声明一个loading对象
    // lock: true,                             // 是否锁屏
    text: text,                     // 加载动画的文字
    // spinner: 'el-icon-loading',             // 引入的loading图标
    // background: 'rgba(0, 0, 0, 0.3)',       // 背景颜色
    target: target,                    // 需要遮罩的区域
    // body: true,
    // customClass: 'mask'                     // 遮罩层新增类名
  })
  setTimeout(function () {                  // 设定定时器，超时5S后自动关闭遮罩层，避免请求失败时，遮罩层一直存在的问题
    loading.close();                        // 关闭遮罩层
  },time_out)
  return loading;
}


Vue.prototype.sleep = function (ms){
  let min = ms * 1000
  return new Promise((resolve)=>setTimeout(resolve,min));
}

Vue.prototype.getClientHeight = function(){
  if(process.server){
    return
  }
  let clientHeight = 0;
  if(document.body.clientHeight&&document.documentElement.clientHeight)
  {
    clientHeight = (document.body.clientHeight<document.documentElement.clientHeight)?document.body.clientHeight:document.documentElement.clientHeight;
  }
  else
  {
    clientHeight = (document.body.clientHeight>document.documentElement.clientHeight)?document.body.clientHeight:document.documentElement.clientHeight;
  }
  return clientHeight;
}


Vue.prototype.deepCopy = function (obj) {
  let _obj = JSON.stringify(obj)
  return JSON.parse(_obj);
}
