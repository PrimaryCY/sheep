<template>
	<div>
		<button v-on:click="add">Add</button>
		<button v-on:click="remove">Remove</button>
		<transition-group name="list" >
    <div v-for="item in items" v-bind:key="item" class="list-item">
      {{ item }}
    </div>
		</transition-group>
	</div>
</template>

<script>

	export default {
		el: '#list-demo',
		data(){
			return {
				items: [1,2,3,4,5,6,7,8,9],
				nextNum: 10
				}
			},
		methods: {
			randomIndex: function () {
				return Math.floor(Math.random() * this.items.length)
			},
			add: function () {
				this.items.splice(this.randomIndex(), 0, this.nextNum++)
			},
			remove: function () {
				this.items.splice(this.randomIndex(), 1)
			},
		}
	}
</script>

<style scoped lang="scss">
	.list-enter-active, .list-leave-active {
		transition: all 1s;
	}
	.list-enter, .list-leave-to
		/* .list-leave-active for below version 2.1.8 */ {
		opacity: 0;
		transform: translateY(30px);
	}

	.list-item{
		width: 100%;
	}
</style>
