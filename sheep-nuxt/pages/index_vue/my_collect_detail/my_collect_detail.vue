<template>
	<div class="wrap">

		<div v-if="not_found" class="not_found">
			<el-page-header @back="push({name:'my_collect'})" content="未找到">
			</el-page-header>
		</div>
		<div v-else class="detail-body">
			<el-page-header @back="push({name:'my_collect'})" content="详情页面">
			</el-page-header>
			my_collect-detail
			{{collect_desc}}
		</div>
	</div>
</template>

<script>
  import {
    api_user_collect_category
  } from '../../../api'

  export default {
    name: 'my_collect_detail',
		data(){
      return {
        not_found:false,
        collect_desc:{

				},
				collect_data:[],
			}
		},
		methods:{
			async _get_collect_desc(){
				// 获取收藏集简介,标题之类的
				let loading = this.openLoading({
					text:'加载中...',
					target:'.wrap'
				})
				let id = this.$route.params.id
				let res = await api_user_collect_category.retrieve(id)
				res =res.data
				if(res.code === 404){
					loading.close()
					return this.not_found = true
				}else if(res.code !== 2000){
					loading.close()
          return this.$message(res.msg)
				}
				this.collect_desc = res.data
				loading.close()
			}
		},
		created () {
      if(process.server)return
			this._get_collect_desc()
    },
		inject:['push']
  }
</script>

<style scoped lang="scss">
	.wrap{
		.not_found{
			width: 100%;
		}
		.detail-body{
			width: 100%;
		}
	}
</style>
