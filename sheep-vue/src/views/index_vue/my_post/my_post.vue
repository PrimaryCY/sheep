<template>
	<div class="my_post">
		<div class="header-filter">
			<el-form :inline="true" class="demo-form-inline">
				<el-form-item label="关键字:">
					<el-input placeholder="文章名称" v-model="params.name"></el-input>
				</el-form-item>
				<el-form-item label="类别:">
					<el-cascader
									ref="cascader"
									:options="option.post_category"
									v-model="post_category"
									:props="{value:'id',label:'name',children:'child'}"
									:show-all-levels="false">
						<template slot-scope="{ node, data }">
							<span>{{ data.name }}</span>
							<span v-if="!node.isLeaf"> ({{ data.child.length }}) </span>
						</template>
					</el-cascader>
				</el-form-item>
				<el-form-item label="创建日期:">
					<el-date-picker
									v-model="created_time_range"
									type="daterange"
									align="right"
									unlink-panels
									range-separator="至"
									start-placeholder="开始日期"
									end-placeholder="结束日期"
									:picker-options="pickerOptions">
					</el-date-picker>
				</el-form-item>
				<el-form-item label="排序方式">
					<el-select v-model="params.order" placeholder="请选择">
						<el-option
										label="点赞"
										value="praise_num"
						></el-option>
						<el-option
										label="阅读"
										value="read_num"
						></el-option>
						<el-option
										label="收藏"
										value="like_num"
						></el-option>
						<el-option
										label="评论"
										value="post_num"
						></el-option>
					</el-select>
				</el-form-item>
				<el-form-item>
					<el-button type="primary">搜索</el-button>
				</el-form-item>
			</el-form>
		</div>
		<div class="article-list">
			<!--增加tabindex属性  使focus对div起作用-->
			<div class="article-list-item-mp" tabindex="0" v-for="post in posts.results" :key="post.id">
				<el-row class="article-title">
					<el-col :span="18">
						<div>
							<a class="article-title-text">{{post.name}}</a>
						</div>
					</el-col>
				</el-row>
				<el-row class="article-info" type="flex">
					<el-col :span="5">
						发表时间:{{post.created_time}}
					</el-col>
					<el-col :span="5">
						更新时间:{{post.update_time}}
					</el-col>
					<el-col :span="2">
						浏览:{{post.read_num}}
					</el-col>
					<el-col :span="2">
						点赞:{{post.praise_num}}
					</el-col>
					<el-col :span="2">
						收藏:{{post.like_num}}
					</el-col>
					<el-col :span="2">
						评论:{{post.post_num}}
					</el-col>
					<el-col :span="4">

					</el-col>
					<el-col :span="2" class="article-btn">
						<el-button size="mini">
							编辑
						</el-button>
					</el-col>
					<el-col :span="2" class="article-btn">
						<el-button size="mini" type="danger">
							删除
						</el-button>
					</el-col>
				</el-row>
			</div>
		</div>
		<div class="footer-pagination">
				<pagination
								@change="_get_user_posts"
								:pagination_config="{layout:'total, sizes, prev, pager, next',background:true}"
								:params="params"
								:pager="posts"></pagination>
		</div>

	</div>
</template>

<script>
	import {mapState} from 'vuex'

	import {user_post} from "../../../api"
	import pagination from '../../../components/pagination'

	export default {
		data() {
			return {
				pickerOptions: {
					shortcuts: [{
						text: '最近一周',
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
							picker.$emit('pick', [start, end]);
						}
					}, {
						text: '最近一个月',
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
							picker.$emit('pick', [start, end]);
						}
					}, {
						text: '最近三个月',
						onClick(picker) {
							const end = new Date();
							const start = new Date();
							start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
							picker.$emit('pick', [start, end]);
						}
					}]
				},
				created_time_range:[],	//筛选日期范围
				post_category:[],				//筛选类别
				params:{
					limit:10,
					offset:0,
					name:null,
					start_created_time:null,
					end_created_time:null,
					category:null,
					order:null,
				},
				posts:{
					total:0,
					results:[]
				}
			}
		},
		mounted() {
			this._get_user_posts()
		},
		methods:{
			async _get_user_posts(){
				// 获取用户个人帖子
				let loading = this.openLoading({
					target:'.my_post'
				})
				let res = await user_post.get(this.params)
				if(res.code!==2000){
					this.$message(res.msg)
					loading.close()
					return
				}
				this.posts=res.data
				loading.close()
			},
			change(){
				this._get_user_posts()
			}
		},
		watch:{
			created_time_range:{
				deep:true,
				handler:function(new_val){
					this.params.start_created_time=new_val[0]
					this.params.end_created_time=new_val[1]
				}
			},
			post_category:{
				deep:true,
				handler:function (new_val) {
					this.params.category=new_val[new_val.length-1]
				}
			}
		},
		computed:{
			...mapState(['option'])
		},
		components:{
			pagination
		}
	}
</script>

<style scoped lang="scss">
	.my_post{
		text-align: left;
		.header-filter{
			padding: 0 20px;
			margin: 0 0 1em 0;
		}
		.article-list{
			min-height: 80vh;
			/*帖子列表*/
			.article-list-item-mp{
				display: -webkit-box;
				display: -ms-flexbox;
				display: flex;
				-webkit-box-direction: normal;
				-webkit-box-orient: vertical;
				-ms-flex-direction: column;
				flex-direction: column;
				border-top: 1px dotted #ddd;
				border-bottom: 1px dotted #ddd;
				padding: 1rem 1rem 1rem 1rem;
				color: #999;
				font-size: 14px;
				transition: background-color 0.25s ease;
				.article-title{
					-webkit-box-orient: horizontal;
					-ms-flex-direction: row;
					flex-direction: row;
					-webkit-box-pack: start;
					-ms-flex-pack: start;
					justify-content: flex-start;
					.article-title-text{
						font-size: 16px;
						color: #4d4d4d;
						margin-bottom: 0;
						-webkit-box-flex: 1;
						-ms-flex-positive: 1;
						flex-grow: 1;
						display: -webkit-box;
						display: -ms-flexbox;
						display: flex;
					}
				}
				.article-info{
					margin-top: 10px;
					display: -webkit-box;
					display: -ms-flexbox;
					font-size: 11px;
					display: flex;
					-webkit-box-orient: horizontal;
					-webkit-box-direction: normal;
					-ms-flex-direction: row;
					flex-direction: row;
					-webkit-box-align: center;
					-ms-flex-align: center;
					align-items: center;
					-webkit-box-pack: justify;
					-ms-flex-pack: justify;
					.article-btn{
						margin: 0 10px;
						border-right: 1px solid #e9e9e9;
					}
				}
			}
			.article-list-item-mp:hover{
				background-color: #f5f7fa;
			}
			.article-list-item-mp:focus{
				background-color: #ecf5ff;
				outline: 0;
				/*outline: -webkit-focus-ring-color auto 1px;*/
			}
		}

		.footer-pagination{
			padding: 8%;
			text-align: center;
		}
		/*.article-list-item-mp:active{*/
		/*	background-color: #000000;*/
		/*}*/

	}

</style>
