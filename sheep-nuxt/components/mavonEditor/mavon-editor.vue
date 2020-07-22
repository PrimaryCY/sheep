<template>
	<div class="home">
		<mavon-editor
						ref="md"
						placeholder="请输入内容..."
						:boxShadow="false"
						:style="{height: this.height}"
						style="z-index:1;border: 1px solid #d9d9d9;"
						v-model="content"
						:ishljs="true"
						:tabSize="4"
						:toolbars="toolbars"
						:editable="this.editable"
						@imgAdd="handleEditorImgAdd"
		/>
	</div>
</template>

<script>
  import Vue from 'vue'

  if(process.client) {
  let mavonEditor = require('mavon-editor')
    require('mavon-editor/dist/css/index.css')
    // require("mavon-editor/dist/highlightjs/highlight.min.js")
    // require('mavon-editor/dist/katex/katex')
    Vue.use(mavonEditor)
  }

	import {api_upload} from "@/api"

	export default {
		name: "home",
		components: {
		},
		props:{
			value:{
				default:''
			},
			height:{
				default:'90vh'
			},
			editable:{
				type:Boolean,
				default:true
			}
		},
		data() {
			return {
				content: this.value,
				toolbars: {
					bold: true, // 粗体
					italic: true, // 斜体
					header: true, // 标题
					underline: true, // 下划线
					strikethrough: true, // 中划线
					mark: true, // 标记
					superscript: true, // 上角标
					subscript: true, // 下角标
					quote: true, // 引用
					ol: true, // 有序列表
					ul: true, // 无序列表
					link: true, // 链接
					imagelink: true, // 图片链接
					code: true, // code
					table: true, // 表格
					fullscreen: true, // 全屏编辑
					readmodel: true, // 沉浸式阅读
					htmlcode: true, // 展示html源码
					help: true, // 帮助
					/* 1.3.5 */
					undo: true, // 上一步
					redo: true, // 下一步
					trash: true, // 清空
					save: false, // 保存（触发events中的save事件）
					/* 1.4.2 */
					navigation: true, // 导航目录
					/* 2.1.8 */
					alignleft: true, // 左对齐
					aligncenter: true, // 居中
					alignright: true, // 右对齐
					/* 2.2.1 */
					subfield: true, // 单双栏模式
					preview: true, // 预览
				},
				upload_data:{
					upload_path:'sheep-post-mavon',
					file:null,
				}
			};
		},
		methods: {
			// 上传图片方法
			async handleEditorImgAdd(pos, $file) {
				let loading = this.openLoading({
					target:'.v-note-edit',
					text:'上传中...'
				})
				this.upload_data.file=$file
				let res = await api_upload.upload(this.upload_data)
        res = res.data
				if(res.code!==2000){
					this.$message(res.msg)
					loading.close()
					return false
				}
				this.$refs.md.$img2Url(pos, res.data.url)
				this.$notify.success('上传成功!')
				loading.close()
			},
		},
		computed:{
			d_render(){
					return this.$refs['md'].d_render
				}
		},
		watch:{
			value(n){
				this.content=n
			},
			content(n){
				this.$emit('input', n)
			},
		}
	};
</script>
<style lang="scss">
	.fullscreen{
		height: 100%!important;
	}
</style>
