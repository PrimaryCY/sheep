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

						<el-col :span="19" >
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
						<el-col :span="2" >
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
											class="sumbit"
											type="primary"
											@click="sumbit"
							>{{submit_btn_text}}</el-button>
						</el-col>
						<el-col :span="3">
							<el-button
											@click="post.content_type=post.content_type===1?2:1">
								{{post.content_type===1?'切换markdown模式':'切换富文本模式'}}
							</el-button>
						</el-col>
					</el-row>

			</el-form>
		</div>
    <no-ssr>
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
	import {api_post_category, api_user_post} from '@/api/index'
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
					if(this.schema==='create'){
						let res = await api_user_post.created(this.post)
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
						let res = await api_user_post.update(this.$route.params.id, this.post)
            res = res.data
						if(res.code!==2000){
							this.$message(res.msg)
							loading.close()
							return
						}
						loading.close()
						this.$message.success('修改成功!')
					}
				}
				)
			},
			async _get_category_data(){
				// 远程获取类别数据
				let res = await api_post_category.list()
        res = res.data
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
      }
			// await this._get_category_data()
			// this._get_default_category()
		},
		components:{
			Backtop,
			tinymceEditor,
			mavon_editor
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
      }
		},
		watch:{
			'option.post_category':{
				deep:true,
				handler:function (n) {
					this.cascader_data.category_data=n
					this._get_default_category()
				}
			},
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
		width: 178px;
		height: 178px;
		display: block;
	}

</style>
