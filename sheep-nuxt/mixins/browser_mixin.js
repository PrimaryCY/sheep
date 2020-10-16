export default {
    name: "browser_mixin",
    provide() {
        return {
            move_to_top: this.move_to_top,
            reload: this.reload,
            push: this.push,
            blank_push: this.blank_push,
            generate_url: this.generate_url,
            blank_inner_window: this.blank_inner_window
        }
    },
    data() {
        return {
            isRouterAlive: true,
        }
    },
    methods: {
        blank_inner_window(url, title, iWidth, iHeight) {
            //window.screen.height获得屏幕的高，window.screen.width获得屏幕的宽
            let iTop = (window.screen.height - 30 - iHeight) / 2       //获得窗口的垂直位置;
            let iLeft = (window.screen.width - 10 - iWidth) / 2        //获得窗口的水平位置;
            window.open(url, title, 'height=' + iHeight + ',,innerHeight=' + iHeight + ',width=' + iWidth + ',innerWidth=' + iWidth + ',top=' + iTop + ',left=' + iLeft + ',toolbar=no,menubar=no,scrollbars=auto,resizeable=no,location=no,status=no')
        },
        move_to_top() {
            // 移动到顶部
            document.body.scrollIntoView({behavior: 'smooth'})
        }
        ,
        blank_push(push_params) {
            // 新窗口打开页面
            let routeData = this.$router.resolve(push_params)
            window.open(routeData.href, '_blank')
        }
        ,
        reload() {
            //刷新当前组件
            this.isRouterAlive = false
            this.$nextTick(function () {
                this.isRouterAlive = true
            })
        }
        ,
        push(url) {
            // 页面跳转
            if (this.$route.path === url) {
                // this.reload()
                return
            }
            this.move_to_top()
            this.$router.push(url)
        }
        ,
        generate_url(params) {
            // 生产反向解析url
            return this.$router.resolve(params).href
        }
    }
}
