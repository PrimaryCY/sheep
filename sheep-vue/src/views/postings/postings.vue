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

					<el-row type="flex">

						<el-col :span="19">
							<el-form-item label="标题:" prop="name">
								<el-input
												type="text"
												placeholder="请输入文章标题"
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
						<el-col :span="2">
							<el-button
											class="sumbit"
											type="info"
											plain
											@click="upload_image.flag = true"
							>文章封面</el-button>
						</el-col>
						<el-col :span="2">
							<el-button
											class="sumbit"
											type="primary"
											@click="sumbit"
							>{{post.type?'保存修改':'发表文章'}}</el-button>
						</el-col>
						<el-col :span="3">
							<el-button
											@click="post.content_type=post.content_type===1?2:1">
								{{post.content_type===1?'切换markdown模式':'切换为富文本模式'}}
							</el-button>
						</el-col>
					</el-row>

			</el-form>
		</div>
		<div v-show="post.content_type===1">
			<tinymce-editor v-model="post.tiny_content"
											ref="tinymce"
											:height="515"
			></tinymce-editor>
			<backtop></backtop>
		</div>
		<div v-show="post.content_type===2">
					<mavon_editor
									ref="mavon"
									v-model="post.mavon_content"
									height="90vh"
					/>
			<backtop target=".v-show-content" @click="mavon_backtop_click"></backtop>
		</div>

		<el-dialog title="文章封面" :visible.sync="upload_image.flag">
			<el-upload
							class="image image-full"
							action=""
							:show-file-list="false"
							:before-upload="before_image_upload">
				<img v-if="reader_image" :src="reader_image" alt="" />
				<i v-else class="el-icon-plus avatar-uploader-icon">上传...</i>
			</el-upload>
			<div slot="footer" class="dialog-footer">
				<el-button @click="upload_image.flag = false">取 消</el-button>
				<el-button type="primary" @click="upload">保 存</el-button>
			</div>
		</el-dialog>
	</div>
</template>

<script>
	import tinymceEditor from '../../components/Tinymce/tinymce-editor'
	import mavon_editor from '../../components/mavonEditor/mavon-editor'
	import {get_post_category,upload,create_user_post} from '../../api/index'
	import Backtop from "../../components/backtop"

	export default {
		name: "postings",
		data(){
			let post={
					name:'',
					category:'',
					image:null,
					content:'',
					tiny_content:'',
					mavon_content:'',
					content_type:1, //true为富文本,false为markdown
					type:false, //true为发表文章,false为编辑文章
			}
			return {
				post,
				reader_image:post.image,
				cascader_data:{		//帖子类别
					category_data:[],
					category:[],
				},
				upload_image:{		//上传封面
					file:post.image,
					upload_path:'post_image',
					flag:false,
				},
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
				}
			}
		},
		methods:{
			mavon_backtop_click(){
				// markdown的回到顶部
				document.getElementsByClassName('v-note-edit')[0].scrollTo({top:0,behavior: "smooth"})
			},
			sumbit(){
				this.$refs['rule_post'].validate(async (valid) => {
					if (!valid) {
						return false;
						}
					this.post.content=this.post.content_type===1?this.post.tiny_content:this.$refs['mavon'] .d_render
					if(!this.post.content){
						return this.$message('文章内容不能为空!')
					}
					this.post.category=this.cascader_data.category
					let res = await create_user_post(this.post)
					if(res.code===2000){
						this.$message.success('发布成功!')
					}
					}
				)
			},
			async _get_category_data(){
				// 远程获取类别数据
				let res = await get_post_category()
				if(res.code===2000){
					this.cascader_data.category_data=res.data
				}else {
					this.$message(res.msg)
				}
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
			before_image_upload(file){
					const isJPG = file.type === "image/jpeg";
					const isPNG = file.type === "image/png";

					if (!isJPG && !isPNG) {
						this.$message.error("上传头像图片只能是 JPG 或 PNG 格式!");
					} else {
						this.upload_image.file=file
						this._image_preview(file);
					}
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
					self.reader_image = e.target.result;
				};
				reader.readAsDataURL(file);
			},
			async upload(){
				if(!this.upload_image.file){
					this.$message('请上传图片!')
					return null
				}
				// 上传修改头像
				let loading = this.openLoading({
					text:'上传中...',
					target:'#el-dialog'
				})
				let res = await upload(this.upload_image)
				if(res.code!==2000){
					this.$message(res.msg)
					loading.close()
					return null
				}
				loading.close()
				this.post.image=res.data.url
				this.upload_image.file=null
				this.$message.success('上传成功!')
				this.upload_image.flag=false
			},
		},
		async created(){
			await this._get_category_data()
			this._get_default_category()
		},
		components:{
			Backtop,
			tinymceEditor,
			mavon_editor
		},
	}
</script>
<style scoped lang="scss">
	.sumbit{
		width: 100%;
	}
	.el-form-item{
		margin-bottom: 17px;
	}
	.post_content{
		/*height: 100%;*/
		background-color: white;
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
		width: 178px;
		height: 178px;
		display: block;
	}

</style>
