	export default {
		name: "browser_mixin",
		provide () {
			return {
				move_to_top:this.move_to_top,
        reload: this.reload,
        push:this.push,
        blank_push:this.blank_push,
			}
		},
		methods:{
			move_to_top(){
				document.body.scrollIntoView({behavior:'smooth'})
			},
      blank_push(push_params){
        // 新窗口打开页面
        let routeData = this.$router.resolve(push_params);
        window.open(routeData.href, '_blank');
      },
      reload () {
        //刷新当前组件
        this.isRouterAlive = false
        this.$nextTick(function () {
          this.isRouterAlive = true
        })
      },
      push(url){
        // 页面跳转
        if(this.$route.path===url){
          // this.reload()
          return
        }
        this.$router.push(url)
      },
		}
	}
