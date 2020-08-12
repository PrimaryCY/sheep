<template>
	<div class="error" >
		<p v-show="message">
			{{message}}
		</p>
	</div>
</template>

<script>
	export default {
		name: "error_message",
		props:['message']
	}
</script>

<style scoped lang="scss">
	.error{
		text-align: left;
		color: #f56c6c;
		font-size: 12px;
		line-height: 1;
		padding-top: 4px;
		top: 100%;
		left: 0;
		display: block;
	}
</style>
