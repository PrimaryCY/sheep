<template>
	<div class="wrap">
		<div class="collect-header">
			<img src="@/static/img/category_title.jpg" class="collect-header-title">
			<div class="collect-header-right">
				<span>
					共 {{categories.length}} 个收藏集
				</span>
			</div>
		</div>
		<div class="content">
			<ul class="collection-list">
				<li class="item">
					<el-card shadow="hover">
						<div class="add">
							<div class="el-icon-plus avatar-uploader-icon cancel-select"
							@click="edit_dialog=!edit_dialog"
							>
								新建收藏集
							</div>
						</div>
					</el-card>
				</li>
				<li class="item" v-for="c in categories" :key="c.id">
					<el-card shadow="hover">
						<div class="bg">
							<img :src="c.image" class="bg-img" @click="collect_push(c.id)">
							<div class="bg-text">
								<div class="title-wrap">
									<div class="title" @click="collect_push(c.id)">
										<p class="ellipsis">{{ c.name }}</p>
									</div>
									<div class="title-icon">
										<font_icon  v-if="c.is_show" :type="5">
										</font_icon>
										<font_icon  v-else :type="6">
										</font_icon>
									</div>
								</div>
								<div class="desc">
									<p class="ellipsis">创建于 {{c.created_time}}</p>
								</div>
								<div class="bottom" style="text-align: end">
									<div class="bottom-text">
										<p>
											共有{{c.total}}个资源
										</p>
									</div>
									<div class="bg-btn">
										<el-button
														type="info"
														plain
														@click="click_edit(c)"
														size="mini">编辑</el-button>
										<el-popconfirm
														confirmButtonText='好的'
														cancelButtonText='取消'
														icon="el-icon-info"
														iconColor="red"
														@onConfirm="delete_func(c)"
														title="这个收藏集确定删除吗(删除操作不可逆)？">
										<el-button
														type="danger"
														plain
														size="mini"
														slot="reference">删除</el-button>
										</el-popconfirm>
									</div>
								</div>
							</div>
						</div>
					</el-card>
				</li>
			</ul>
			<el-dialog
							@close="click_dialog_cancle"
							:modal-append-to-body=false
							top="2vh"
							custom-class="edit-dialog"
							:visible.sync="edit_dialog">
				<el-form :model="collect_form" :rules="collect_rules" ref="collect_form" label-width="100px">
					<el-form-item label-width="0" prop="image" class="upload-image">
						<el-upload
										class="avatar-uploader"
										action="https://"
										:show-file-list="false"
										:before-upload="before_image_upload">
							<img v-if="reader_portrait ||collect_form.image" :src="reader_portrait || collect_form.image" class="image">
							<i v-else class="el-icon-plus avatar-uploader-icon image" ></i>
						</el-upload>
					</el-form-item>
					<el-form-item label="名称" prop="name" size="mini">
						<el-input  v-model="collect_form.name" :maxlength="100" show-word-limit></el-input>
					</el-form-item>
					<el-form-item label="是否公开" prop="resource" size="mini">
						<el-radio-group v-model="collect_form.is_show">
							<el-radio :label="true">公开</el-radio>
							<el-radio :label="false">隐藏</el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="简介" prop="desc" size="mini">
						<el-input type="textarea"
											v-model="collect_form.desc"
											:maxlength="500"
											show-word-limit></el-input>
					</el-form-item>
					<el-form-item size="mini">
						<el-button @click="edit_dialog=!edit_dialog">取消</el-button>
						<el-button type="primary" @click="click_dialog_comfirm">提交</el-button>
					</el-form-item>
				</el-form>
			</el-dialog>
		</div>
	</div>
</template>

<script>
	import {
			api_upload,
			api_user_collect_category
			} from '../../../api'
  import font_icon from '@/components/small/font_icon'

  export default {
    name: 'my_collect',
		data(){
      return{
        categories:[],
				edit_dialog:false,
				collect_form:{
					name:'',
					desc:'',
					image:'',
					is_show:true,
				},
				uploadData:{
					file:null,
          upload_path:'sheep-portrait',
				},
        reader_portrait:'',
				collect_rules:{
        name:[
          {
            required:true, message: '请输入收藏集名称!', trigger: 'change'//触发条件：blur、change
          }]}
			}
		},
		methods:{
      collect_push(id){
        // 跳转收藏集详情页面
        this.push({name:'my_collect_detail', params:{id}})
			},
      async _get_collect_category(){
        // 初始化收藏集列表
				let cate = await api_user_collect_category.list()
				cate = cate.data
				if(cate.code !== 2000)return this.$message(cate.msg)
				this.categories = cate.data
			},
			async delete_func(collect){
        // 删除收藏集
				let res = await api_user_collect_category.destory(collect.id)
				res = res.data
				if(res.code!==2000){
					this.$message(res.msg)
					return null
				}
				this.$message.success('删除成功!')
				this._get_collect_category()
      },
			click_edit(collect){
        this.collect_form = collect
				this.edit_dialog = true
			},
      click_dialog_comfirm(){
        // 新增或修改点击确认
        this.$refs['collect_form'].validate(async (valid) => {
          if(!valid){
            return null
					}
          let loading = this.openLoading({
						text:'提交中...',
						target:'.edit-dialog',
						time_out:10000
					})
          // 上传封面
          if(this.reader_portrait){
						let res = await api_upload.upload(this.uploadData)
						res = res.data
						if(res.code!==2000){
							loading.close()
							this.$message('上传失败!请重试!')
							return null
						}
						this.collect_form.image = res.data.url
					}
          let col_res
          if(this.collect_form.id){
            // 修改收藏集
            col_res = await api_user_collect_category.update(this.collect_form.id, this.collect_form)
					}
          else {
            // 新建收藏集
            col_res = await api_user_collect_category.create(this.collect_form)
					}
          col_res = col_res.data
          if(col_res.code!==2000){
            loading.close()
            this.$message(col_res.msg)
						return null
					}
          this.$message.success('提交成功')
          loading.close()
          this.edit_dialog = !this.edit_dialog
					this._get_collect_category()
        });
			},
			click_dialog_cancle(){
        // dialog关闭时,重置数据
				this.collect_form = {is_show:true}
				this.reader_portrait = null
        this.edit_dialog = false
			},
      before_image_upload(file) {
        const isJPG = file.type === "image/jpeg";
        const isPNG = file.type === "image/png";

        if (!isJPG && !isPNG) {
          this.$message.error("上传封面图片只能是 JPG 或 PNG 格式!");
        }
				else {
          this.uploadData.file=file
          this._image_preview(file);
          this.uploadData.flag=true
        }
        return false;
      },
      _image_preview: function(file) {
        var self = this;
        var reader = new FileReader();
        reader.onload = function(e) {
          //将bade64位图片保存至数组里供上面图片显示
          self.reader_portrait = e.target.result;
        };
        reader.readAsDataURL(file);
      },
		},
		async created () {
      if(process.server)return
			await this._get_collect_category()
    },
		components:{
      font_icon
		},
		inject:['push','move_to_top']
  }
</script>

<style scoped lang="scss">
	/deep/ .edit-dialog{
		text-align: initial;
		font-size: 10px;
	}
	/deep/ textarea{
		min-height: 80px!important;
	}

	.upload-image{
		text-align: center;
		.image{
			width: 200px;
			height: 200px;
			background-repeat: no-repeat;
			line-height: 200px;
			border-radius: 2px;
			object-fit: cover;
		}
	}

	.el-form-item{
		margin-bottom: 2px;
	}

	.el-card.is-always-shadow, .el-card.is-hover-shadow:focus, .el-card.is-hover-shadow:hover{
		box-shadow: 5px 2px 12px 5px rgba(4,4,4,.1);
	}
	.el-card /deep/ .el-card__body{
		padding: 5px !important;
		border-radius: 25%;
	}
	.collect-header{
		display: flex;
		align-items: center;
		flex-wrap: wrap;
		padding: 0 2.4rem;
		height: 4.167rem;
		white-space: nowrap;
		border-bottom: 1px solid rgba(230,230,231,.5);
		.collect-header-title{
			height: 100%;
			margin-right: 1rem;
			font-size: 1.25rem;
			font-weight: 600;
			color: #000;
		}
		.collect-header-right{
			margin-left: auto;
		}
	}

	.collection-list{
		padding: 2rem 0.5rem;
		display: flex;
		justify-content: space-around;
		align-items: center;
		flex-wrap: wrap;
		.item{
			margin-bottom: .8rem;
			width: calc(31% - .4rem);
			margin: 0 0 1.4rem;
			box-sizing: border-box;
			.bg{
				transition: .3s;
				.bg-img{
					width: 270px;
					height: 270px;
					border-radius: 5px;
					object-fit: cover;
					cursor: pointer;
				}
				.bg-text{
					text-align: left;
					padding: 5px 20px;

					.title-wrap{
						position: relative;
						.title{
							font-weight: bold;
							margin-right: 50px;
							font-size: 15px;
							cursor: pointer;
							p{
								margin-bottom: 0;
							}
						}
						.title:hover{
							color: #b53c57;
						}
						.title-icon{
							position: absolute;
							right: 0;
							top: 0;
						}
					}
					.desc{
						font-size: 12px;
						p{
							margin-bottom: 0;
						}
					}
					.bottom{
						clear: both;
						.bottom-text{
							font-size: 10px;
							float: left;
							color: grey;
						}
						.bg-btn{
							float: right;
							margin-bottom: 5px;
						}
					}
				}
			}
			.add{
				width: 270px;
				height: 350px;
				cursor: pointer;
				div{
					line-height: 350px;
					width: 100%;
					height: 100%;
					font-weight: bold;
				}
			}
		}
	}
</style>
