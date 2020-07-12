<template>
	<div class="post_content">
		<div >
			<el-form
							ref="rule_post"
							:model="post"
							:rules="post_rules"
							label-width="70px"
							status-icon
							label-position="'left">

					<el-row type="flex" :gutter="2">

						<el-col :span="17" >
							<el-form-item label="标题:" prop="name">
								<el-input
												type="text"
												:placeholder="name_placeholder"
												v-model="post.name"
												width="1200px"
												maxlength="100"
												show-word-limit
								></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="3">
							<el-form-item label-width="0">
								<el-cascader
												ref="cascader"
												:options="cascader_data.category_data"
												v-model="cascader_data.category"
												:props="{value:'id',label:'name',children:'child'}"
												:show-all-levels="false">
									<template slot-scope="{ node, data }">
										<span>{{ data.name }}</span>
										<span v-if="!node.isLeaf"> ({{ data.child.length }}) </span>
									</template>

								</el-cascader>
							</el-form-item>
						</el-col>
						<el-col :span="3" >
							<div class="post_type_select">
								<el-form-item label-width="0" prop="post_type">
									<el-radio-group
													size="mini"
													v-model="post.post_type">
										<el-radio	:label="1">文章</el-radio>
										<el-radio :label="2">提问</el-radio>
									</el-radio-group>
								</el-form-item>
							</div>
						</el-col>

            <el-col :span="2">
              <el-button
                class="fullwidth"
                @click="dialog=true">
                {{image_text}}
              </el-button>
            </el-col>

						<el-col :span="2">
							<el-button
											class="sumbit"
											type="primary"
											@click="sumbit"
							>{{submit_btn_text}}</el-button>
						</el-col>

						<el-col :span="3">
							<el-button
                      class="fullwidth"
											@click="post.content_type=post.content_type===1?2:1">
								{{post.content_type===1?'切换markdown模式':'切换富文本模式'}}
							</el-button>
						</el-col>
					</el-row>

			</el-form>
		</div>
    <el-dialog :visible.sync="dialog">
      <div class="dialog">
        <el-upload
          class="avatar-uploader"
          action=""
          :show-file-list="false"
          :before-upload="before_avatar_upload">
          <img v-if="reader_portrait" :src="reader_portrait" class="avatar">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
        <bubble_text
          text="建议上传580*263的图片哟👍"
          position="right">
        </bubble_text>
        <bubble_text
          text="上传图片,你的文章/提问才能上轮播推荐哦👍"
          position="right">
        </bubble_text>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="destory_image">删除</el-button>
        <el-button @click="dialog = false">取 消</el-button>
        <el-button type="primary" @click="upload_image">提 交</el-button>
      </div>
    </el-dialog>
    <no-ssr>
		<div v-show="post.content_type===1">
        <tinymce-editor v-model="post.tiny_content"
                        ref="tinymce"
                        :height="getClientHeight()*0.93"
        ></tinymce-editor>
			<backtop></backtop>
		</div>
		<div v-show="post.content_type===2">
					<mavon_editor
									ref="mavon"
									v-model="post.mavon_content"
									height="91vh"
					/>
			<backtop target=".v-show-content" @click="mavon_backtop_click"></backtop>
		</div>
    </no-ssr>
	</div>
</template>

<script>
	import {mapState} from 'vuex'

	import tinymceEditor from '../../components/Tinymce/tinymce-editor'
	import mavon_editor from '../../components/mavonEditor/mavon-editor'
  import bubble_text from '@/components/common/bubble_text'
	import {api_post_category, api_user_post, api_upload} from '@/api/index'
	import Backtop from "../../components/backtop"

	export default {
		name: "postings",
		data(){
			let post={
					name:'',
					category:'',
					image:null,
					html_content:'',
					content:'',
					tiny_content:'',
					mavon_content:'',
					content_type:1, //true为富文本,false为markdown
					post_type:1, //1为文章,2为提问
			}
			return {
				schema: 'create', //当前模式
				post,
				cascader_data:{		//帖子类别
					category_data:[],
					category:[],
				},
        dialog:false, // 提交按钮框
				post_rules:{
					'name':[
						{required:true,message:'请输入标题!',trigger:'change'},
						{
							validator:(r,v,c)=>{
								if(!v.trim()){
									c(new Error('请输入标题!'))
								}else {
									c()
								}
							}, trigger: 'change'
						}
					],
				},
        reader_portrait: null,
				upload_data:{
          upload_path:'post_image',
          file: undefined,
        }
			}
		},
		methods:{
      destory_image(){
        this.reader_portrait=undefined
        this.post.image=null
        this.upload_data.file=undefined
      },
      async upload_image(){
        let loading = this.openLoading({
          text:'上传中...',
          target:'.dialog'
        })
        let res = await api_upload.upload(this.upload_data)
        if(res.data.code!==2000){
          this.$message(res.data.msg)
          loading.close()
          return
        }
        this.post.image=res.data.data.url
        this.dialog=!this.dialog
        this.$message.success('上传成功!')
        loading.close()
      },
      before_avatar_upload(file) {
        const isJPG = file.type === "image/jpeg";
        const isPNG = file.type === "image/png";
        const isLt1M = file.size / 1024 / 1024 < 1;

        if (!isJPG && !isPNG) {
          this.$message.error("上传头像图片只能是 JPG 或 PNG 格式!");
        } else if (!isLt1M) {
          this.$message.error("上传头像图片大小不能超过 1MB!");
        } else {
          this.upload_data.file=file
          this._image_preview(file);
        }
        // 不使用upload自带的上传方式，而是使用axios，所以阻止upload自带的上传
        return false;
      },
      _image_preview: function(file) {
        // 图片预览
        var self = this;
        //定义一个文件阅读器
        var reader = new FileReader();
        //文件装载后将其显示在图片预览里
        reader.onload = function(e) {
          //将bade64位图片保存至数组里供上面图片显示
          self.reader_portrait = e.target.result;
        };
        reader.readAsDataURL(file);
      },
			mavon_backtop_click(){
				// markdown的回到顶部
				document.getElementsByClassName('v-note-edit')[0].scrollTo({top:0,behavior: "smooth"})
			},
			sumbit(){
				this.$refs['rule_post'].validate(async (valid) => {
					if (!valid) {
						return false;
						}
					let loading = this.openLoading({
						'text':'发布中...'
					})
					// 根据编辑器不同,获取不同的原始数据
					if(this.post.content_type===1){
						this.post.html_content = this.post.tiny_content
						this.post.content = this.$refs['tinymce'].get_content()
					}else {
						this.post.html_content = this.$refs['mavon'].d_render
						this.post.content = this.post.mavon_content
					}
					if(!this.post.html_content){
						return this.$message('内容不能为空!')
					}
					this.post.category=this.cascader_data.category
          let res
					if(this.schema==='create'){
						res = await api_user_post.create(this.post)
            res = res.data
						if(res.code!==2000){
							this.$message(res.msg)
							loading.close()
							return
						}
						loading.close()
						this.$message.success('发布成功!')
					}
					else {
						res = await api_user_post.update(this.$route.params.id, this.post)
            res = res.data
						if(res.code!==2000){
							this.$message(res.msg)
							loading.close()
							return
						}
						loading.close()
						this.$message.success('修改成功!')
					}
					this.$router.replace({name:'post_detail',params:{id:res.data.id}})
				}
				)
			},
			_get_category_data(){
				// 远程获取类别数据
				// let res = await api_post_category.list()
        // res = res.data
				// if(res.code===2000){
				// 	this.cascader_data.category_data=res.data
				// }else {
				// 	this.$message(res.msg)
				// }
        this.cascader_data.category_data = this.option.post_category
			},
			_get_default_category(){
				function _get_first_cascader_node(data,res=[]) {
					for(let i of data){
						res.push(i['id'])
						if(!i.child||!i.child.length){
								return res
						}else {
								return _get_first_cascader_node(i['child'],res)
							}
						}
					}
				if(!this.post.category){
					// 默认获取第一个子节点
					this.cascader_data.category=_get_first_cascader_node(this.cascader_data.category_data)
					}else {
					this.cascader_data.category=this.post.category
					}
				},
			async _select_schema(){
				// 选择当前模式
				let id = this.$route.params.id
				if(id){
					let loading = this.openLoading({
						'text':'加载中...'
					})
					let res = await api_user_post.retrieve(id)
          res = res.data
					if(res.code!==2000) {
						this.$message(res.msg)
						loading.close()
						return
					}
					this.post = res.data
          this.reader_portrait = this.post.image
					if(res.data.content_type===1){
						this.post.tiny_content = this.post.parse_content
					}else {
						this.post.mavon_content = this.post.parse_content
					}
					this.cascader_data.category = this.post.category_list
					this.schema = 'update'
					loading.close()
				}else {
					this.schema = 'create'
				}
			}
		},
		async created(){
      if(process.client){
        await this._select_schema()
        this._get_category_data()
        this._get_default_category()
      }
    },
		components:{
			Backtop,
			tinymceEditor,
			mavon_editor,
      bubble_text
		},
		computed:{
			...mapState(['option']),
			name_placeholder(){
				return this.post.post_type===1?'请输入标题...':'请填写提问...'
			},
      submit_btn_text(){
        if(this.schema==='create'){
          if(this.post.post_type===1){
            return '发表'
          }else {
            return '提问'
          }
        }else {
          return '保存'
        }
      },
      image_text(){
        return this.post.post_type===1?'文章封面':'问题封面'
      },
		},
	}
</script>
<style scoped lang="scss">
  .dialog{
    text-align: center;
  }
	.sumbit{
		width: 100%;
	}
	.el-form-item{
		margin-bottom: 17px;
	}
	.post_content{
		/*height: 100%;*/
		background-color: white;
		.post_type_select{
			text-align: center;
		}
	}
	.el-radio{
		margin-right: 0!important;
	}
	.el-form-item__content{
		margin-left: 0!important;
	}

	.image-full{
		text-align: center;
	}
	.avatar-uploader .el-upload {
		border: 1px dashed #d9d9d9;
		border-radius: 6px;
		cursor: pointer;
		position: relative;
		overflow: hidden;
	}
	.avatar-uploader .el-upload:hover {
		border-color: #409EFF;
	}
	.avatar-uploader-icon {
		font-size: 15px;
		color: #8c939d;
		width: 178px;
		height: 178px;
		line-height: 178px;
		text-align: center;
	}
	.avatar {
		width: 580px;
		height: 263px;
		display: block;
	}

</style>
