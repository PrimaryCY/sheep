<template>
	<div>
		<el-table
						:data="tableData"
						stripe
						:border="true"
						highlight-current-row
						style="width: 100%">
			<el-table-column
							type="index"
							width="50">
			</el-table-column>
			<el-table-column
							prop="date"
							label="日期"
							width="180">
			</el-table-column>
			<el-table-column
							prop="name"
							label="姓名"
							width="180">
			</el-table-column>
			<el-table-column
							prop="address"
							:filters="[{ text: '家', value: '家' }, { text: '公司', value: '公司' }]"
							:filter-method="filterTag"
							label="地址">
			</el-table-column>
			<el-table-column label="操作">
				<template slot-scope="scope">
					<el-button
									size="mini"
									@click="handleEdit(scope.$index, scope.row)">编辑</el-button>
					<el-button
									size="mini"
									type="danger"
									@click="handleDelete(scope.$index, scope.row)">删除</el-button>
				</template>
			</el-table-column>
		</el-table>
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

<style scoped>

</style>
