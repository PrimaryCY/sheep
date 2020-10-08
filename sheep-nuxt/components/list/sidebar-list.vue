<template>
  <div class="list">
    <h3 class="title">
      <span class="line"></span>
      <span class="txt">
              {{title}}
      </span>
    </h3>
    <a
      v-for="(i, index) in list"
      :key="i.id"
      :href="$router.resolve({name:'post_detail',params:{id:i.id}}).href"
      target="_blank"
      class="sidebar-list-item">
      <div v-if="i.image" class="img-box">
        <img :src="i.image">
      </div>
      <div class="content">
        <h2 class="company_name">
          <slot name="item-content" :item="i" :index="index">

          </slot>
        </h2>
      </div>
    </a>
  </div>
</template>

<script>
  export default {
    name: 'sidebar-item',
    props:{
      list:{
        // 列表
        type:Array,
        required:true
      },
      title:{
        // 标题
        type:String,
        required:true
      }
    },
  }
</script>

<style scoped lang="scss">
  .list{
    .title{
      display: -webkit-box;
      display: -ms-flexbox;
      display: flex;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      font-size: 16px;
      color: #4a4a4a;
      height: 24px;
      line-height: 24px;
      margin-bottom: 5px;
      position: relative;
      .line{
        display: block;
        float: left;
        width: 3px;
        height: 16px;
        background: #cf2730;
        overflow: hidden;
        margin-right: 5px;
      }
      .txt{
        display: block;
        float: left;
        font-size: 16px;
        color: #2c3033;
      }
    }
    .sidebar-list-item {
      /*margin-bottom: 10px;*/
      overflow: hidden;
      /*min-height: 52px;*/
      height: 50px;
      display: block;
      border-bottom: 1px solid #e4e7ed;
      .img-box {
        float: left;
        position: relative;
        img {
          cursor: pointer;
          position: relative;
          /*display: inline-block;*/
          display: block;
          width: 64px;
          height: 44px;
          border-radius: 3px;
          vertical-align: top;
          -o-object-fit: cover;
          object-fit: cover;
        }
      }

      .content {
        padding-top: 2px;
        .company_name{
          display: block;
          margin-bottom: 3px;
          font-size: 12px;
          color: #3d3d3d;
          letter-spacing: 0;
          line-height: 22px;
          //max-width: 200px;
          overflow: hidden;
          cursor: pointer;
          font-weight: bold;
          text-overflow: -o-ellipsis-lastline;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          line-clamp: 2;
          -webkit-box-orient: vertical;
        }
      }
    }
  }
  .sidebar-list-item:hover{
      background-color: #f5f7fa;
    .content{
      .company_name{
        color: #b53c57;
      }
    }
  }

</style>
