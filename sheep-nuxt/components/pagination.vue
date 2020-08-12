<template>
<!--	<div class="block" :style="{ 'white-space': 'nowrap','padding': '2px 5px','color': '#303133','font-weight': '700','text-align': 'center' }">-->
	<div>
		<el-pagination
						:background="pagination.background"
						:layout="pagination.layout"
						:total="pager.count"
						:current-page.sync="currentPage"
						:page-size="params.limit"
						:page-sizes="pagination.page_sizes"
						prev-text="上一页"
						next-text="下一页"
						:hide-on-single-page="pagination.hide_on_single_page"
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
					hide_on_single_page:true,
				}
			}
		},
		props: {
			// 每页返回数据
			'pager':{
				type:Object,
				required:true
			},
			// 查询参数
			'params':{
				type:Object,
				required:true
			},
			pagination_config:{
				type:Object,
				required:false
			},
		},
		computed: {
			pagination(){
				return Object.assign(this.pagination_default_config, this.pagination_config)
			},
			// // 检测是否获取到无数据
			// initBack() {
			// 	return this.pager.total / this.pager.offset < this.pager.page;
			// },
		},
		watch: {
			// total() {
			// 	// 存在记录但未获取到数据时, 重新请求
			// 	if (this.initBack) {
			// 		this.params.offset -= 1;
			// 		this.$emit('change');
			// 	}
			// },
		},
		mounted() {},
		methods: {
      reset_params(){
        this.params.offset = 0
        this.currentPage = 1
      },
			// 每页条数
			onChangeSize(rows) {
				this.currentPage = 1
				this.params.offset = 0
				this.params.limit = rows;
				this.$emit('change');
			},
			// 翻页
			onChangePage(page) {
        console.log(page)
				this.params.offset = (this.params.limit*page)-this.params.limit;
				this.$emit('change');
			}
		}
	}
</script>
