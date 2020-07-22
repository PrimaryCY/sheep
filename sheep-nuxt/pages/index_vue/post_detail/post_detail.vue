<template>
  <div class="wrap">
      <div class="left" :style="{'margin-right':pack_up?'150px':'190px'}">
        <div v-if="response.code===404">
          404
        </div>
        <div class="article" v-else-if="data.post_type===1" >
          <div class="article-title">
            <h1>
              {{data.name}}
            </h1>
            <div class="article-info"
                 :class="{'is_fixed' : isFixed}"
                 id="boxFixed">
              <el-row type="flex">
<!--                <el-col :span="2">-->
<!--                  <div class="on">-->
<!--                    <font_icon :type="data.post_type"></font_icon>-->
<!--                  </div>-->
<!--                </el-col>-->
                <el-col :span="2">
                  <div class="on">
                    <svg class="icon-mid"  aria-hidden="true">
                      <use xlink:href="#icon-liulan"></use>
                    </svg>
                    {{data.read_num}}
                  </div>
                </el-col>
                <el-col :span="2">
                  <div class="on pointer">
                    <svg class="icon-mid" style="width: 18px;height: 20px;" aria-hidden="true">
                      <use xlink:href="#icon-icon_community_line"></use>
                    </svg>
                    {{data.post_num}}
                  </div>
                </el-col>

                <el-col :span="5" :offset="11">
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
              <el-divider></el-divider>
            </div>
          </div>
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
        <div v-else-if="data.post_type===2"></div>
      </div>
      <div class="right">
        <div class="author-info-wrap" v-if="data.author_info">
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
</template>

<script>
  import {api_post, api_category_post, api_correlation_category, api_author_post} from '../../../api'
  import {mapState } from 'vuex'
  import font_icon from '../../../components/small/font_icon'
  import tinymceEditor from '../../../components/Tinymce/tinymce-editor'
  import {get_tree_first_node} from '../../../utils/util'

  export default {
    name: 'post_detail',
    data(){
      return {
        response:{    //文章内容具体响应,包含code值
        },
        data:{        // 文章内容
          author_info:{}
        },
        reply_form:{  //评论
          placeholder:'请输入回复内容...'
        },
        correlation_category:{  //相关分类
        },
        author_post:{       //作者其它文章
        },
        category_post:{     //相同分类下文章
        },
        isFixed:false,    //吸顶
        offsetTop: 0,     //吸顶

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
      let id,post_res,detail_recommend_list
      id = context.params.id
      let return_dict = {}
      // try {
        post_res = await api_post.retrieve(id)
        post_res = post_res.data

        return_dict['data'] = post_res.data?post_res.data:{}
        return_dict['response'] = post_res

        if(post_res.code===404){
          let c, corr_res, cate_post_res;
          console.log(context.store.state.option)
          c = get_tree_first_node(context.store.option.post_category)
          console.log(c)
          detail_recommend_list = [
            api_correlation_category.list({id:c}),
            api_category_post.list({category:c})
          ];
          [corr_res, cate_post_res] = await Promise.all(detail_recommend_list);
          return_dict['correlation_category'] = corr_res.data.data;
          return_dict['category_post'] = cate_post_res.data.data;
        }else {
          let corr_res, au_post_res, cate_post_res
          detail_recommend_list = [
            api_correlation_category.list({id:post_res.data.category_id}),
            api_author_post.list({author_id:post_res.data.author_id}),
            api_category_post.list({category:post_res.data.category_id})
          ];
					[corr_res, au_post_res, cate_post_res] = await Promise.all(detail_recommend_list)
          return_dict['correlation_category'] = corr_res.data.data;
					return_dict['author_post'] = au_post_res.data.data;
					return_dict['category_post'] = cate_post_res.data.data;
        }
      // }catch(e)
      // {
        // context.error({statusCode:500,message:'ssr internal server error'})
      // }
      return return_dict
    },
    methods:{
      initHeight() {
        // 文章顶部栏吸顶效果
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
        this.isFixed = scrollTop-15 > this.offsetTop ? true : false;
        if(this.isFixed){
          let width = document.getElementsByClassName('left')[0].clientWidth
          document.getElementById('boxFixed').style.width = `${width}px`
        }else {
          document.getElementById('boxFixed').style.width = 'initial'
        }
      },
    },
    mounted() {
      window.addEventListener('scroll', this.initHeight);
      this.$nextTick(() => {
        let el = document.querySelector('#boxFixed');
        if(el) this.offsetTop = el.offsetTop
      })
    },
    destroyed() {
      window.removeEventListener('scroll', this.handleScroll)
    },
  }
</script>

<style scoped lang="scss">
  /* 吸顶 */
  .is_fixed{
    position: fixed;
    top: 0;
    z-index: 999;
    margin: 0;
    padding: 0!important;
    background-color: white;
    .el-divider--horizontal{
      margin-top: 5px;
      margin-bottom: initial!important;
    }
  }
  .el-divider--horizontal{
    margin-top: 5px;
  }
  .wrap{
    position: initial!important;
    height: 100%;
    .left{
      height: 100%;
      /*margin-right: 180px;*/
      margin-left: -30px;
      .article{
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
            .num_data{
              border-radius: 25%;
            }
            .num_data:hover{
              background-color: #ecf5ff;
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

</style>
