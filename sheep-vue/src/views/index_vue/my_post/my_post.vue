<template>
	<div class="my_post">
		<div class="header-filter">
			<el-form :inline="true" class="demo-form-inline">
				<el-form-item label="审批人">
					<el-input placeholder="审批人"></el-input>
				</el-form-item>
				<el-form-item label="活动区域">
					<el-select placeholder="活动区域">
						<el-option label="区域一" value="shanghai"></el-option>
						<el-option label="区域二" value="beijing"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item>
					<el-button type="primary">查询</el-button>
				</el-form-item>
			</el-form>
		</div>
		<div class="article-list">
			<!--增加tabindex属性  使focus对div起作用-->
			<div class="article-list-item-mp" tabindex="0" v-for="i in 15">
				<el-row class="article-title">
					<el-col :span="18">
						<div>
							<a class="article-title-text">我是文章的大标题</a>
						</div>
					</el-col>
				</el-row>
				<el-row class="article-info" type="flex">
					<el-col :span="5">
						2019年06月17日 11:19:36
					</el-col>
					<el-col :span="2">
						点赞:138
					</el-col>
					<el-col :span="2">
						收藏:138
					</el-col>
					<el-col :span="2">
						收藏:138
					</el-col>
					<el-col :span="9">

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
			<el-pagination
							background
							layout="prev, pager, next"
							:total="1000">
			</el-pagination>
		</div>

	</div>
</template>

<script>
	export default {
		data() {
			return {
				tableData: [{
					date: '2016-05-02',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1518 弄'
				}, {
					date: '2016-05-04',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1517 弄'
				}, {
					date: '2016-05-01',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1519 弄'
				}, {
					date: '2016-05-03',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1516 弄'
				}]
			}
		}
	}
</script>

<style scoped lang="scss">
	.my_post{
		text-align: left;
		.header-filter{
			padding: 0 20px;
			margin: 0 0 2em 0;
		}
		.article-list{
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
						font-size: 19px;
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
