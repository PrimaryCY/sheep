<template>
  <div class="wrap">
    <div class="article" v-if="data.post_type===1">
      <div class="left">
        <div class="article-title">
          <h1>
            {{data.name}}
          </h1>
          <div class="article-info">
            <el-row>
              <el-col :span="5" :offset="13">
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
        <div class="article-content">
          <div v-html="data.html_content">
          </div>
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
        </div>
      </div>
    </div>
    post-{{$route.params.id}}
  </div>
</template>

<script>
  import {api_post} from '../../../api'

  export default {
    name: 'post_detail',
    data(){
      return {
        data:{}
      }
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
      console.log(res.data.data)
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
        margin-right: 180px;
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
        .article-content{
          text-align: initial;
        }
      }
      .right{
        position: absolute;
        right: 0;
        top: 0;
        width: 240px;
        height: 100%;
        .author-info-wrap{
          border-bottom: 1px solid #EBEEF5;
          border-left: 1px solid #EBEEF5;
          margin-top: 10px;
          height: 100px;
          .author-info{
            color: #1a1a1a;
            font-weight: 500;
            h1{
              margin-top: 10px;
            }
          }
        }
      }
    }
  }

</style>
