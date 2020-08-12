	export default {
		name: "browser_mixin",
		provide () {
			return {
				move_to_top:this.move_to_top,
        reload: this.reload,
        push:this.push,
        blank_push:this.blank_push,
        generate_url:this.generate_url
			}
		},
    data(){
      return {
        isRouterAlive:true,
      }
    },
		methods:{
			move_to_top(){
        // 移动到顶部
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
        this.move_to_top()
        this.$router.push(url)
      },
      generate_url(params){
        // 生产反向解析url
        return this.$router.resolve(params).href
      }
		}
	}
