<template>
	<div class="zwsj" v-if="list&&list.length===0">
		<img :src="img" :width="width" :height="height"/>
		<div style="color: #999;font-size: 12px;margin-top: 5px">{{text}}</div>
	</div>
</template>

<script>
	export default {
		name: "not-data",
		props: {
			img: {
				default: './static/img/not_data.png',
				require: false
			},
			text: {
				require: false
			},
			width: {
				default: "80%"
			},
			height: {
				default: "80%"
			},
			list:{
				required:true
			}
		}
	}
</script>

<style scoped>
	.zwsj {
		/*padding: 120px 0;*/
		text-align: center;
	}
</style>
