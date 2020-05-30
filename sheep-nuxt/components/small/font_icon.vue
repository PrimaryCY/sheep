<template>
		<a v-if="type===2" class="article-question-type" >
			<svg class="icon-min" aria-hidden="true">
				<use xlink:href="#icon-wenti--copy"></use>
			</svg>
			问题
		</a>
		<a v-else-if="type===1" class="article-post-type">
			<svg class="icon-min" aria-hidden="true">
				<use xlink:href="#icon-shiyongwendang"></use>
			</svg>
			文章
		</a>
</template>

<script>
	export default {
		name: "post_type",
		props:{
			type:{
				type:Number,
				required:true
			}
		}
	}
</script>

<style scoped lang="scss">
		.article-question-type{
			display: inline;
			border-radius: 25%;
			width: 7%;
			text-align: center;
			font-size: x-small;
			color: white;
			opacity: .7;
			background-color: #b02727;
			margin: 0 5px 0 0;
		}
		.article-post-type{
			display: inline;
			border-radius: 25%;
			width: 7%;
			opacity: .7;
			text-align: center;
			font-size: x-small;
			color: white;
			background-color: #795548;
			margin: 0 5px 0 0;
		}
</style>
