<template>
    <router-view v-if="isRouterAlive" ></router-view>
</template>

<script>
    import {mapState} from 'vuex'

    import setting from './conf/settings'


    export default {
        name: 'app',
        provide () {
            return {
                reload: this.reload,
                push:this.push,
                blank_push:this.blank_push,
            }
        },
        data () {
            return {
                isRouterAlive: true
            }
        },
        computed:{
            ...mapState(['user'])
        },
        methods: {
            blank_push(name, query){
                // 新窗口打开页面
                let routeData = this.$router.resolve({
                    name: name,
                    query: query
                });
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
                    this.reload()
                    return
                }
                this.$router.push(url)
            },
            async _get_user_info(){
                // 获取token中保存的登录信息
                if(this.$cookies.get(setting.TOKEN_NAME)&&!this.user.username){
                    let loading = this.openLoading({
                        text:'自动登录中..'
                    })
                    this.$store.dispatch('receive_userinfo',()=>{
                        loading.close()
                    })
                }
            },
            _debugger(){
                // 全局设置vue实例
                if(setting.DEBUG){
                    window._v=this
                }
            }
        },
        created(){
            this._get_user_info()
            this._debugger()
        },
    }
</script>

<style >
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        zoom: .8;

        /*仿chrome缩放*/
        /*-webkit-transform: scale(.8,.8) !important;*/
        /*-webkit-transform-origin: 0 0!important;*/
    }

    [v-cloak] {
        display: none;
    }

    /*修改element的默认样式*/
    .el-message-box__wrapper .message{
        width: 300px!important;
    }
</style>
