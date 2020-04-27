<template>
		<div class="tbe">
			<img :src='img_src' alt="" />
			<h2><b>{{text}}</b></h2>
		</div>

</template>

<script>
	export default {
		name: "tbe",
		data(){
			return{
			}
		},
		props:{
			'text':{
				default:'敬请期待!'
			},
			'img_src':{
				default: require('../../public/static/img/tbe.gif')
			}
		}
	}
</script>

<style scoped lang="scss">
	.tbe{
		text-align: center;
		img{
			width: 80%;
			height: 80%;
		}
	}

</style>
