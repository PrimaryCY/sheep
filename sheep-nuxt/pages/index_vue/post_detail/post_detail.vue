<template>
  <div class="wrap">
    <div class="article" v-if="data.post_type===1">
      <div class="left" :style="{'margin-right':pack_up?'150px':'190px'}">
        <div class="article-title">
          <h1>
            {{data.name}}
          </h1>
          <div class="article-info">
            <el-row type="flex">
              <el-col :span="2">
                <div class="on">
                  <font_icon :type="data.post_type"></font_icon>
                </div>
              </el-col>
              <el-col :span="2">
                <div class="on">
                  <svg class="icon-mid" aria-hidden="true">
                    <use xlink:href="#icon-liulan"></use>
                  </svg>
                    {{data.read_num}}
                </div>
              </el-col>
              <el-col :span="5" :offset="9">
                <span class="byline">
                  发布时间:{{data.created_time}}
                </span>
              </el-col>
              <el-col :span="1">
                <div class="divider">
                  |
                </div>
              </el-col>
              <el-col :span="5">
                <span class="byline">
                更新时间:{{data.update_time}}
                </span>
              </el-col>
            </el-row>
          </div>
        </div>
        <el-divider></el-divider>
        <div class="article-content-wrap">
          <div  class="article-content" v-html="data.html_content">
          </div>
          <el-divider></el-divider>
          <no-ssr placeholder="Loading...">
            <tinymce-editor v-model="reply_form.html_content"
                            ref="tinymce"
                            :height="260"
                            :menubar="false"
                            toolbar="reply_toolbar"
                            :statusbar="false"
                            :placeholder="reply_form.placeholder"
            ></tinymce-editor>
          </no-ssr>
        </div>
      </div>
      <div class="right">
        <div class="author-info-wrap">
            <a class="ellipsis author-info pointer">
              <el-avatar
                class="vertical-middle"
                :size="60"
                :src="data.author_info.portrait">
              </el-avatar>
              <h1>{{data.author_info.username}}</h1>
            </a>
          <span>年龄: {{data.author_info.age}}</span>
          <span>网站年龄: {{data.author_info.website_age}}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {api_post} from '../../../api'
  import {mapState } from 'vuex'
  import font_icon from '../../../components/small/font_icon'
  import tinymceEditor from '../../../components/Tinymce/tinymce-editor'

  export default {
    name: 'post_detail',
    data(){
      return {
        data:{},
        reply_form:{
          placeholder:'请输入回复内容...'
        }
      }
    },
    components:{
      font_icon,
      tinymceEditor
    },
    computed:{
      ...mapState(['pack_up'])
    },
    async asyncData(context){
      let id,res
      id = context.params.id
      try {
        let async_list = [
          api_post.retrieve(id),
        ];
        [res] = await Promise.all(async_list)
      }catch(e)
      {
        context.error({statusCode:500,message:'ssr internal server error'})
      }
      return {
        data:res.data.data
      }
    },
    methods:{

    },
    created () {
      // if(process.client){
      //   document.getElementById('content').style.padding = '0'
      // }
    }

  }
</script>

<style scoped lang="scss">

  .el-divider--horizontal{
    margin-top: 5px;
  }
  .wrap{
    position: initial!important;
    height: 100%;
    .article{
      height: 100%;
      .left{
        height: 100%;
        /*margin-right: 180px;*/
        margin-left: -30px;
        .article-title{
          padding: 10px 0;
          h1{
            font-size: 28px;
            word-wrap: break-word;
            color: #222226;
            line-height: 33px;
            font-weight: 600;
            margin: 0;
            word-break: break-all;
          }
          .article-info{
            font-size: 11px;
            .on{
              margin-top: 1em;
              svg{
                vertical-align: bottom;
              }
            }
            .byline{
              text-align: right;
            }
            .divider{
              margin-top: 1em;
              line-height: 100%;
              font-size: 15px;
              text-align: right;
            }
          }
        }
        .article-content-wrap{
          text-align: initial;
          .article-content{
            min-height: 40vh;
            *{
              font-size: initial;
              margin: initial;
              border: initial;
              font-weight: initial;
              vertical-align: initial;
            }
          }
        }
      }
      .right{
        position: absolute;
        right: 0;
        top: 0;
        width: 240px;
        height: 100%;
        border-left: 1px ridge darkgray;
        .author-info-wrap{
          border-bottom: 1px solid #EBEEF5;
          border-left: 1px solid #EBEEF5;
          margin-top: 10px;
          .author-info{
            color: #1a1a1a;
            font-weight: 500;
            h1{
              margin: 10px;
            }
          }
        }
      }
    }
  }

</style>
