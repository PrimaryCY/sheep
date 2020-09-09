<template>
  <div class="article-list-item-mp">
  <el-row class="article-title">
    <el-col>
      <div v-if="post.image" class="article-image">
        <img :src="post.image">
      </div>
      <div class="article-title-text" @click="blank_push_post_detail(post)">
        {{post.name}}
      </div>
      <span class="article-desc byline ellipsis">
        {{post.desc}}
      </span>
    </el-col>
  </el-row>
  <el-row class="article-info">
    <el-col :span="2">
      <font_icon :type="post.post_type"></font_icon>
    </el-col>
    <el-col :span="5">
      {{post.post_type===1?'创建':'提问'}}时间:{{post.created_time}}
    </el-col>
    <el-col :span="5">
      更新时间:{{post.update_time}}
    </el-col>
    <el-col :span="2">
      <svg class="icon-min" aria-hidden="true">
        <use xlink:href="#icon-liulan"></use>
      </svg>
      :{{post.read_num}}
    </el-col>
    <el-col :span="2">
      <svg class="icon-min" aria-hidden="true">
          <use :xlink:href="post.praise_num < 0 ? '#icon-cai-copy':'#icon-icon_likegood'"></use>
      </svg>
      :{{post.praise_num}}
    </el-col>
    <el-col :span="2">
      <svg class="icon-min" aria-hidden="true">
        <use xlink:href="#icon-shoucang"></use>
      </svg>
      :{{post.like_num}}
    </el-col>
    <el-col :span="2">
      <svg class="icon-min" aria-hidden="true">
        <use xlink:href="#icon-icon_community_line"></use>
      </svg>
      :{{post.post_num}}
    </el-col>
    <el-col :span="4">
      <!--占位使用-->
    </el-col>
    <el-col v-if="post.status===0&&editor" :span="2" class="article-btn">
      <el-button
        plain
        type="info"
        @click="update_func(post)"
        size="mini">
        编辑
      </el-button>
    </el-col>
    <el-col v-if="post.status===0&&editor" :span="2" class="article-btn">
      <el-popconfirm
        confirmButtonText='好的'
        cancelButtonText='不用了'
        icon="el-icon-info"
        iconColor="red"
        @onConfirm="delete_func(post)"
        :title="`您确定删除${post.post_type===1?'此文章':'此问题'}吗？`"
      >
        <el-button
          size="mini"
          type="danger"
          slot="reference">删除</el-button>
      </el-popconfirm>
    </el-col>
    <el-col :span="5" v-if="post.status !== 0" class="article-btn delete_msg">
      {{ delete_text }}
    </el-col>
  </el-row>
  </div>
</template>

<script>
  import font_icon from '../../small/font_icon'

  export default {
    name: 'post_item',
    props:{
      post:{
        type:Object,
        required:true
      },
      editor:{
        type:Boolean,
        default(){
          return false
        }
      },
    },
    components:{
      font_icon
    },
    methods:{
      delete_func(post){
        this.$emit('delete_func',post)
      },
      update_func(post){
        this.$emit('update_func', post)
      },
      blank_push_post_detail(post){
        if(post.status!==0){
          return this.$message(`此${post.post_type===1?'文章':'问题'}已被删除!`)
        }
        this.blank_push({name:'post_detail',params:{id:post.id}})
      }
    },
    inject:['blank_push'],
    computed:{
      delete_text(){
        let text;
        if(this.post.post_type===1){
          if(this.post.status===1){
            text = '文章已被您删除'
          }else if(this.post.status===2){
            text = '文章已被管理员删除'
          }else if(this.post.status===3)
            text = '由于点赞过低已被删除'
          else if(this.post.status===4){
            text = '由于内容违规已被删除'
          }
        }else {
          if(this.post.status ===1){
            text = '问题已被您删除'
          } else if(this.post.status===2){
            text = '问题已被管理员删除'
          }else if(this.post.status===3)
            text = '由于点赞过低已被删除'
          else if(this.post.status===4){
            text = '由于内容违规已被删除'
          }
      }
      return `${text}❌!`
      }
    }
  }
</script>

<style scoped lang="scss">

    .article-title{
      -webkit-box-orient: horizontal;
      -ms-flex-direction: row;
      flex-direction: row;
      -webkit-box-pack: start;
      -ms-flex-pack: start;
      justify-content: flex-start;
      .article-image{
        float: left;
        margin-right: 5px;
        img{
          vertical-align:text-top;
          width: 100px;
          height: 45px;
          object-fit: cover
        }
      }
      .article-title-text{
        font-size: 16px;
        color: #4d4d4d;
        margin-bottom: 0;
        -webkit-box-flex: 1;
        -ms-flex-positive: 1;
        flex-grow: 1;
        cursor: pointer;
      }
      .article-desc{
        font-size: 10px!important;
        display: -webkit-box;
        margin-top: initial;
      }
      .article-title-text:hover{
        color: #b53c57;
      }
    }
    .article-info{
      margin-top: 10px;
      display: -webkit-box;
      display: -ms-flexbox;
      font-size: 11px;
      display: flex;
      -webkit-box-orient: horizontal;
      -webkit-box-direction: normal;
      -ms-flex-direction: row;
      flex-direction: row;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      -webkit-box-pack: justify;
      -ms-flex-pack: justify;
      .article-btn{
        margin: 0 10px;
        border-right: 1px solid #e9e9e9;
      }
      .delete_msg{
        border: 0!important;
        color: #F56C6C;
        text-align: center;
      }
    }

</style>
