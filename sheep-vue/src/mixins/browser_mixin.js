	export default {
		name: "browser_mixin",
		provide () {
			return {
				move_to_top:this.move_to_top,
			}
		},
		methods:{
			move_to_top(){
				document.body.scrollIntoView({behavior:'smooth'})
			}
		}
	}
