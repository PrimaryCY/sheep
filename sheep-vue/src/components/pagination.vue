<template>
<!--	<div class="block" :style="{ 'white-space': 'nowrap','padding': '2px 5px','color': '#303133','font-weight': '700','text-align': 'center' }">-->
	<div>
		<el-pagination
						:background="pagination.background"
						:layout="pagination.layout"
						:total="pager.count"
						:current-page.sync="currentPage"
						:page-size="pager.rows"
						:page-sizes="pagination.page_sizes"
						prev-text="上一页"
						next-text="下一页"
						@size-change="onChangeSize"
						@current-change="onChangePage">
		</el-pagination>
	</div>
</template>
<script>
	export default {
		name: 'Pagination',
		data(){
			return {
				currentPage:1,
				pagination_default_config:{
					layout:"total, sizes, prev, pager, next, jumper",
					page_sizes:[5,10,15,20],
					background:false,
				}
			}
		},
		props: {
			'pager':{
				type:Object,
				required:true
			},
			pagination_config:{
				type:Object,
				required:false
			},
		},
		computed: {
			total() {
				return this.pager.total;
			},
			pagination(){
				return Object.assign(this.pagination_default_config, this.pagination_config)
			},
			// 检测是否获取到无数据
			initBack() {
				return this.pager.total / this.pager.offset < this.pager.page;
			},
		},
		watch: {
			total() {
				// 存在记录但未获取到数据时, 重新请求
				if (this.initBack) {
					this.pager.page -= 1;
					this.$emit('change');
				}
			},
		},
		mounted() {},
		methods: {
			// 每页条数
			onChangeSize(rows) {
				this.pager.offset = rows;
				this.$emit('change');
			},
			// 翻页
			onChangePage(page) {
				this.pager.page = page;
				this.$emit('change');
			}
		}
	}
</script>
