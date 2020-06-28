<template>
	<div class="my_post">
		<div class="header-filter">
			<el-form  label-position="left">
				<el-row type="flex" :gutter="20">
					<el-col :span="16">
						<el-form-item
										label-width="60px"
										label="关键字:">
							<el-input placeholder="问题名称"
												clearable
												size="small"
												maxlength="100"
												show-word-limit
												v-model="form.search"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="6">
						<el-form-item
										label-width="45px"
										label="类别:">
							<el-cascader
											ref="cascader"
											clearable
											size="small"
											:options="option.post_category"
											v-model="form.post_category"
											:props="{value:'id',label:'name',children:'child'}"
											:show-all-levels="false">
								<template slot-scope="{ node, data }">
									<span>{{ data.name }}</span>
									<span v-if="!node.isLeaf"> ({{ data.child.length }}) </span>
								</template>
							</el-cascader>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row type="flex" :gutter="20">
					<el-col :span="12">
						<el-form-item
										label-width="75px"
										label="创建日期:">
							<el-date-picker
											v-model="form.created_time_range"
											type="daterange"
											align="right"
											unlink-panels
											range-separator="至"
											start-placeholder="开始日期"
											value-format="yyyy-MM-dd"
											end-placeholder="结束日期"
											size="small"
											:picker-options="pickerOptions">
							</el-date-picker>
						</el-form-item>
					</el-col>
					<el-col :span="7">
						<el-form-item
										label-width="75px"
										label="排序方式:">
							<el-select	v-model="form.ordering"
													clearable
													size="small"
													placeholder="请选择">
								<el-option
												label="点赞(正排序)"
												value="praise_num"
								></el-option>
								<el-option
												label="点赞(倒排序)"
												value="-praise_num"
								></el-option>
								<el-option
												label="阅读(正排序)"
												value="read_num"
								></el-option>
								<el-option
												label="阅读(倒排序)"
												value="-read_num"
								></el-option>
								<el-option
												label="收藏(正排序)"
												value="like_num"
								></el-option>
								<el-option
												label="收藏(倒排序)"
												value="-like_num"
								></el-option>
								<el-option
												label="评论(正排序)"
												value="post_num"
								></el-option>
								<el-option
												label="评论(倒排序)"
												value="-post_num"
								></el-option>
							</el-select>
						</el-form-item>
					</el-col>
					<el-col :span="5">
						<el-form-item>
							<el-button type="primary" @click="filter_post" size="small">查询</el-button>
							<el-button type="danger" @click="form={}" size="small">重置</el-button>
						</el-form-item>
					</el-col>
				</el-row>
			</el-form>
		</div>
		<div class="article-list">
			<!--增加tabindex属性  使focus对div起作用-->
			<transition-group
							tag="div">
			<div class="article-list-item-mp" tabindex="0" v-for="post in posts.results" :key="post.id">
					<el-row class="article-title">
            <el-col :span="3">
              <div v-if="post.image" class="article-image">
                <img :src="post.image">
              </div>
            </el-col>
						<el-col :span="18">
								<div class="article-title-text">
									{{post.name}}
								</div>
						</el-col>
					</el-row>
					<el-row class="article-info" type="flex">
            <el-col :span="2">
              <font_icon :type="post.post_type"></font_icon>
            </el-col>
						<el-col :span="5">
							提问时间:{{post.created_time}}
						</el-col>
						<el-col :span="5">
							更新时间:{{post.update_time}}
						</el-col>
						<el-col :span="2">
							<svg class="icon-min" aria-hidden="true">
								<use xlink:href="#icon-liulan"></use>
							</svg>
							:{{post.read_num}}
						</el-col>
						<el-col :span="2">
							<svg class="icon-min" aria-hidden="true">
								<use xlink:href="#icon-icon_likegood"></use>
							</svg>
							:{{post.praise_num}}
						</el-col>
						<el-col :span="2">
							<svg class="icon-min" aria-hidden="true">
								<use xlink:href="#icon-shoucang"></use>
							</svg>
							:{{post.like_num}}
						</el-col>
						<el-col :span="2">
							<svg class="icon-min" aria-hidden="true">
								<use xlink:href="#icon-icon_community_line"></use>
							</svg>
							:{{post.post_num}}
						</el-col>
						<el-col :span="4">
							<!--占位使用-->
						</el-col>
						<el-col v-if="post.is_active" :span="2" class="article-btn">
							<el-button
											plain
											type="info"
											@click="update_post(post)"
											size="mini">
								编辑
							</el-button>
						</el-col>
						<el-col v-if="post.is_active" :span="2" class="article-btn">
							<el-popconfirm
											confirmButtonText='好的'
											cancelButtonText='不用了'
											icon="el-icon-info"
											iconColor="red"
											@onConfirm="delete_post(post)"
											title="您确定删除这篇提问吗？"
							>
								<el-button
												size="mini"
												type="danger"
												slot="reference">删除</el-button>
							</el-popconfirm>
						</el-col>
						<el-col :span="1" class="article-btn" v-if="!post.is_active">
							<!--占位使用-->
						</el-col>
						<el-col :span="3" v-if="!post.is_active" class="article-btn delete_msg">
								问题已删除!
						</el-col>
					</el-row>
			</div>
			</transition-group>
			<not_data :list="posts.results"></not_data>
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

	import {api_user_post} from "../../../api"
	import pagination from '../../../components/pagination'
	import not_data from '../../../components/not_data'
	import font_icon from '../../../components/small/font_icon'

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
				form:{
					ordering:null,
					search:null,
					post_category:null,
					created_time_range:[],
				},
				params:{
					limit:10,
					offset:0,
					name:null,
					start_created_time:null,
					end_created_time:null,
					category:null,
					ordering:null,
					post_type:2,
				},
				posts:{
					total:0,
					results:null
				}
			}
		},
		mounted() {
			this._get_user_posts()
		},
		methods:{
			update_post(post){
				// 用户按下编辑按钮时
				this.blank_push({
					'name':'postings_detail',
					'params':{id:post.id}
				})
			},
			async delete_post(post){
				//用户按下删除按钮时
				let res = await api_user_post.destory(post.id)
        res = res.data
				if(res.code!==2000){
					return this.$message(res.msg)
				}
        // eslint-disable-next-line require-atomic-updates
				post.is_active=false
				// let ind = this.posts.results.indexOf(post)
				// this.posts.results.splice(ind,1)
			},
			filter_post(){
				// 点击查询
				if(this.form.created_time_range){
					this.params.start_created_time=this.form.created_time_range[0]
					this.params.end_created_time=this.form.created_time_range[1]
				}else{
					this.params.start_created_time=null
					this.params.end_created_time=null
				}
				if(this.form.post_category){
					this.params.category=this.form.post_category[this.form.post_category.length-1]
				}else {
					this.params.category=null
				}
				this.params.ordering = this.form.ordering
				this.params.search = this.form.search
				this._get_user_posts()
			},
			async _get_user_posts(){
				this.move_to_top()
				// 获取用户个人帖子
				let loading = this.openLoading({
					target:'.my_post'
				})
				let res = await api_user_post.list(this.params)
        res = res.data
        console.log(res)
				if(res.code!==2000){
					this.$message(res.msg)
					loading.close()
					return
				}
				// console.log(res.data)
				this.posts=res.data
				loading.close()
			},
		},
		computed:{
			...mapState(['option'])
		},
		components:{
			pagination,
			not_data,
			font_icon
		},
		inject:['blank_push', 'move_to_top']
	}
</script>

<style scoped lang="scss">
	.v-enter,.v-leave-to{
		opacity: 0;
		transform: translateX(-60px);
	}
	.v-enter-active,
	.v-leave-active{
		transition: all 0.6s ease;
	}

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
				/*与vue动画冲突*/
				/*transition: background-color 0.25s ease;*/
				.article-title{
					-webkit-box-orient: horizontal;
					-ms-flex-direction: row;
					flex-direction: row;
					-webkit-box-pack: start;
					-ms-flex-pack: start;
					justify-content: flex-start;
          .article-image{
            img{
              width: 100px;
              height: 100px;
            }
          }
					.article-title-text{
						font-size: 16px;
						color: #4d4d4d;
						margin-bottom: 0;
						-webkit-box-flex: 1;
						-ms-flex-positive: 1;
						flex-grow: 1;
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
					.delete_msg{
						border: 0!important;
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
