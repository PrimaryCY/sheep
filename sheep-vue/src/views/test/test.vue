<template>
	<div>
		<el-form ref="rule_post"
							:model="post" :rules="post_rules" label-width="70px" label-position="'left">
			<el-form-item label="标题:" prop="name">
				<el-input
								type="text"
								placeholder="请输入帖子标题"
								v-model="post.name"
								maxlength="100"
								show-word-limit
				>
				</el-input>
			</el-form-item>
		</el-form>
		<tinymce-editor v-model="post.content"
										@input="input"
										:height="700"
										ref="editor"
			></tinymce-editor>
<!--		<mavon_editor v-model="post.content"/>-->
		<!--		<el-input-->
		<!--						type="text"-->
		<!--						placeholder="请输入帖子标题"-->
		<!--						v-model="post.content"-->
		<!--						maxlength="100"-->
		<!--						show-word-limit-->
		<!--		>-->
		<!--		</el-input>-->
		<!--		<error_message :message="post_error.content"></error_message>-->
		<el-button type="primary" v-show="post_error.flag">提交</el-button>
		<div style="position: fixed;bottom: 0;background-color: red;width: 100px;height: 100px"></div>
	</div>
</template>

<script>
	import tinymceEditor from '../../components/Tinymce/tinymce-editor'
	import mavon_editor from '../../components/mavonEditor/mavon-editor'

	export default {
		name: "postings",
		data(){
			return {
				post_error:{
					flag:false,
				},
				post:{
					name:'',
					content:'',
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
					]
				}
			}
		},
		methods:{
			input(){
				console.log('用户在输入了!')
			}
		},
		components:{
			tinymceEditor,
			mavon_editor
		},
		watch: {
			'post.name': function () {
				console.log(this.$refs['rule_post'])
				this.$refs['rule_post'].validate((valid) => {
						if (!valid) {
							this.post_error.flag = false
							return false;
						}
						this.post_error.flag=true
					}
				)
			}
		}
	}
</script>

<style scoped lang="scss">

</style>
