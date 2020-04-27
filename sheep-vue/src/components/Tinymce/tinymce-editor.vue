<template>
	<div class="tinymce-box">
		<editor v-model="myValue"
						:init="init"
						:disabled="disabled"
						@onClick="onClick">
		</editor>
	</div>
</template>

<script>
	import tinymce from 'tinymce/tinymce' //tinymce默认hidden，不引入不显示
	import Editor from '@tinymce/tinymce-vue'
	import 'tinymce/themes/silver'

	import plugins from './plugins.js'
	import toolbar from './toolbar.js'
	// 更多插件参考：https://www.tiny.cloud/docs/plugins/

	import {upload} from "../../api"

	export default {
		components:{
			Editor
		},
		name:'tinymce',
		props: {
			id: {
				type: String,
				default: function() {
					return 'vue-tinymce-' + +new Date() + ((Math.random() * 1000).toFixed(0) + '')
				}
			},
			value: {
				type: String,
				default: ''
			},
			disabled: {
				type: Boolean,
				default: false
			},
			toolbar: {
				type: Array,
				default(){
					return toolbar
				}
			},
			height: {
				type: [Number, String],
				required: false,
				default: 360
			},
			width: {
				type: [Number, String],
				required: false,
				default: 'auto'
			},
			menubar: {
				type:Boolean,
				required:false,
				default:true
			}
		},
		data(){
			return{
				upload_data:{
					upload_path:'post_tinymce',
					file:null,
				},
				tinymceId: this.id,
				init: {
					selector: `#${this.tinymceId}`,
					// 文件的指定根目录,仅对未指定url的参数有效
					base_url: './static/tinymce/',
					skin_url: './static/tinymce/skins/ui/oxide/',
					emoticons_database_url: './static/tinymce/plugins/emojis/emojis.js',
					language_url: './static/tinymce/langs/zh_CN.js',
					language: 'zh_CN',
					nonbreaking_force_tab: true, // tab缩进
					theme:'silver',
					// skin_url: require('tinymce/skins/ui/oxide-dark/skin.css'),//暗色系
					height: this.height,
					min_height: this.height,
					width:this.width,
					plugins: plugins,
					toolbar: this.toolbar,
					menubar: true,
					draggable_modal: false, // 模态窗口允许拖动
					browser_spellcheck: true, // 拼写检查
					branding: false, // 不去水印
					elementpath: true,  //禁用编辑器底部的状态栏
					statusbar: true, // 隐藏编辑器底部的状态栏
					paste_data_images: true, // 允许粘贴图像
					link_list: [
						{ title: '百度', value: 'http://www.baidu.com' },
						{ title: '新浪', value: 'http://www.sina.com' }
					],
					image_list: [
						{ title: '预置图片1', value: 'http://127.0.0.1:8000/media/portrait/9c38048c08994072acf49af7669fe7e9.png' },
						{ title: '预置图片2', value: 'http://127.0.0.1:8000/media/portrait/9c38048c08994072acf49af7669fe7e9.png' }
					],
					object_resizing: true,
					// 此处为图片上传处理函数，这个直接用了base64的图片形式上传图片，
					automatic_uploads:true,
					images_upload_handler: async (blobInfo, success,failure) => {
						// const img = 'data:image/jpeg;base64,' + blobInfo.base64()
						this.upload_data.file=blobInfo.blob()
						let res = await upload(this.upload_data)
						if(res.code===2000){
							this.$notify.success('上传成功!')
							success(res.data.url)
						}else {
							failure(res.msg)
						}
					},
					file_picker_types: 'file image media', // 可以接受的上传文件类型
					file_picker_callback: (callback) => {
						//文件分类
						let filetype='.pdf, .txt, .zip, .rar, .7z, .doc, .docx, .xls, .xlsx, .ppt, .pptx, .mp3, .mp4, .png';
						//模拟出一个input用于添加本地文件
						let input = document.createElement('input');
						input.setAttribute('type', 'file');
						input.setAttribute('accept', filetype);
						input.click();
						let self = this
						input.onchange =async function f() {
							let loading = self.openLoading({
								text:'上传中...',
								target:'div'
							})
							console.log(self)
							self.upload_data.file= this.files[0]
							let res = await upload(self.upload_data)
							if (res.code !== 2000) {
								self.$message(res.msg)
								loading.close()
								return;
								}
							self.$notify.success('上传成功!')
							loading.close()
							callback(res.data.url);
							};
					}
				},
				myValue: this.value
			}
		},
		mounted () {
			tinymce.init(this.init)
		},
		methods: {
			// 需要什么事件可以自己增加
			onClick (e) {
				this.$emit('onClick', e, tinymce)
			},
			// 可以添加一些自己的自定义事件，如清空内容
			clear () {
				this.myValue = ''
			},
			destroy_tinymce(){
				const tinymce = window.tinymce.get(this.tinymceId)
				if (this.fullscreen) {
					tinymce.execCommand('mceFullScreen')
				}
				if (tinymce) {
					tinymce.destroy()
				}
			}
		},
		watch: {
			value (newValue) {
				this.myValue = newValue
			},
			myValue (newValue) {
				console.log('tinymce的用户输入了!')
				this.$emit('input', newValue)
			}
		},
		deactivated() {
			this.destroy_tinymce()
		},
		destroyed() {
			this.destroy_tinymce()
		}
	}

</script>
<style lang="scss">
	.tox-fullscreen{
		width: 100%!important;
		height: 100%!important;
	}
</style>
