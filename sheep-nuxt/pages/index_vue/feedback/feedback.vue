<template>
  <div class="feedback">
    <div class="feedback-header">
      <p class="header-img">
        <img src="@/static/img/feedback_title.jpg">
      </p>
      <div class="header-content">
        <p>
          🎉感谢您使用sheep！请告诉我们您对sheep的意见和建议，
        </p>
        <p>
          我们会参考您的反馈不断优化我们的产品和服务。
        </p>
      </div>

    </div>
    <div class="feedback-content">
      <el-tabs type="card">
        <el-tab-pane label="🔨提出意见" >
          <el-form  label-width="80px" :model="form"
                    ref="fb_form"
                    :rules="rules"
                    label-position="top" size="mini">
              <el-form-item label="问题类别:" size="mini" prop="category_id">
                <el-radio-group v-model="form.category_id">
                  <el-radio v-for="c in feedback_category"
                            :key="c.id"
                            :label="c.id">
                    {{c.name}}
                  </el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label-width="8px" prop="html_content">
                  <p>问题描述:</p>
                  <no-ssr placeholder="Loading...">
                    <tinymce-editor v-model="form.html_content"
                                    ref="tinymce"
                                    :height="340"
                                    :menubar="false"
                                    :toolbar="'simple_toolbar'"
                                    placeholder="在这里请写下您宝贵的意见,我们会加油努力改进哒!"
                    ></tinymce-editor>
                  </no-ssr>
              </el-form-item>
              <el-form-item label="联系方式(注明一下是手机号/微信/qq号,方便我们联系):" prop="contact_way">
                <el-input v-model="form.contact_way"></el-input>
              </el-form-item>
            <el-form-item size="large" style="text-align: center" label-width="0px">
              <el-button @click="$refs['fb_form'].resetFields()">
                重置
              </el-button>
              <el-button type="primary" @click="sumbit">
                提交
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="📃历史反馈">
          <div class="feedback-list">
            <!--增加tabindex属性  使focus对div起作用-->
            <transition-group tag="div">
              <div class="feedback-list-item-mp" tabindex="0" v-for="fb in feedbacks.results" :key="fb.id">
              </div>
            </transition-group>
            <not_data text='空空如也😭'
                      :list="feedbacks.results"></not_data>
          </div>
          <div class="footer-pagination">
            <pagination
              @change="_get_history_fb"
              :pagination_config="{layout:'total, sizes, prev, pager, next',background:true}"
              :params="params"
              :pager="feedbacks"></pagination>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
  import {mapState} from 'vuex'

  import pagination from '@/components/pagination'
  import not_data from '@/components/not_data'
  import tinymceEditor from '../../../components/Tinymce/tinymce-editor'
  import {api_feedback_category,api_feedback} from '../../../api'

  export default {
    name: 'feedback',
    data(){
      return {
        feedback_category:[],
        form:{
          html_content:'',
          content:'',
          category_id:undefined,
          contact_way:'',
        },
        rules:{
          category:[{required:true,message:'你忘了选反馈类别了呢😋!',trigger:'blur'}],
          html_content:[{required:true,message:'你忘了输入问题详细内容呢😘!',trigger:'blur'}],
          contact_way:[{required:true,message:'亲,留个微信号吧😙!',trigger:'blur'}]
        },
        params:{
          limit:10,
          offset:0,
        },
        feedbacks:{
          total:0,
          results:null
        }
      }
    },
    methods:{
      async _get_category() {
        if (process.client) {
          let res = await api_feedback_category.list()
          res = res.data
          if (res.code !== 2000) {
            this.Message(res.msg)
            return null
          }
          this.feedback_category = res.data
        }
      },
      async sumbit(){
        this.$refs['fb_form'].validate(async (valid) => {
          if (!valid) {
            return false;
          }
          let loading = this.openLoading(
            {
              'text':'提交中',
              'target':'.el-tabs__content',
            }
          )
          this.form.content = this.$refs['tinymce'].get_content()
          let res = await api_feedback.created(this.form)
          res = res.data
          if(res.code!==2000){
            loading.close()
            this.$message(res.msg)
            return null
          }
          loading.close()
          this.$message.success('提交成功,之后注意查看回复哦!')
        })
      },
      async _get_history_fb(){

      }
    },
    async created(){
      await this._get_category()
    },
    computed:{
      ...mapState(['user'])
    },
    components:{
      tinymceEditor,
      pagination,
      not_data
    }
  }
</script>

<style scoped lang="scss">

	.feedback {
    .feedback-header{
      margin-bottom: 5px;
      .header-img {
        margin-bottom: 0;
        text-align: center;
        img{
          width: 22%;
          height: 22%;
        }
      }
      .header-content{
        background-color: #fffbec;
        color: #888;
        border-top: 1px #f6f1dc solid;
        padding: 11px 26px 11px 15px;
        p{
          margin-bottom: 1px;
        }
      }
    }
    .feedback-content{
      margin: 0;
      padding: 0;
      text-align: initial;
      font-size: 18px;
    }
  }
</style>
