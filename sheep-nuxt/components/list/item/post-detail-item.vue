<template>

	<div class="item-wrap">
		<div class="title">
			<div v-if="post.image" class="img-box">
				<img :src="post.image">
			</div>
			<div class="two-line-ellipsis">{{post.name}}</div>
		</div>
		<div class="desc" style="clear: both">
				<div class="icon-box">
					<svg class="icon-min" aria-hidden="true">
                        <use :xlink:href="post.praise_num < 0 ? '#icon-cai-copy':'#icon-icon_likegood'"></use>
					</svg>
					{{post.praise_num}}
				</div>
				<div class="icon-box">
					<svg class="icon-min" aria-hidden="true">
						<use xlink:href="#icon-shoucang"></use>
					</svg>
					{{post.like_num}}
				</div>
		</div>

	</div>
</template>

<script>
  export default {
    name: 'post-detail-item',
		props:{
      post:{
        type:Object,
        required:true
			}
		}
  }
</script>

<style scoped lang="scss">
	.item-wrap{
		color: #333;
        margin-top: 8px;
        border-bottom: 1px solid #EBEEF5;
		.title{
			padding-top: 5px;
			.img-box{
				float: left;
                margin-right: 8px;
				img {
					cursor: pointer;
					position: relative;
					/*display: inline-block;*/
					display: block;
					width: 64px;
					height: 44px;
					border-radius: 3px;
					vertical-align: top;
					-o-object-fit: cover;
					object-fit: cover;
				}
			}
			h1{
				color: #333;
			}
		}
		.desc{
			margin-top: 3px;
			.icon-box{
				display: inline-block;
				margin: 1px 5px 10px 5px;
				font-weight: initial!important;
                border-radius: 5px;
			}
		}
	}
	.item-wrap:hover{
		/*color: #b53c57;*/
	}

</style>
