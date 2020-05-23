<template>
	<div>
		<el-backtop :target="target" @click="click($event)">
<!--			<div-->
<!--							style="{-->
<!--        height: 100%;-->
<!--        width: 100%;-->
<!--        background-color: #f2f5f6;-->
<!--        box-shadow: 0 0 6px rgba(0,0,0, .12);-->
<!--        text-align: center;-->
<!--        line-height: 40px;-->
<!--        color: #1989fa;-->
<!--      }"-->
<!--			>-->
<!--				UP-->
<!--			</div>-->
		</el-backtop>
	</div>
</template>

<script>
	export default {
		// 封装element回到顶部
		name: "backtop",
		props:{
			target:{
				default:null
			},
		},
		methods:{
			click(el){
				this.$emit('click',el)
			}
		}
	}
</script>

<style scoped>

</style>
