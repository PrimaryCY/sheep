<template>
    <!--  <img style="width:100%;height:100%" src="~/Images/chatBack.jpg">-->
    <div class="container">
        <div class="applications">

                <button
                        v-for="a in this.user_oauth" class="item" :key="a.id"
                        type="button">
                        <span class="mat-button-wrapper">
                            <img :src="a.image"/>
                        </span>
                </button>

        </div>
    </div>

</template>

<script>
import {mapState} from 'vuex'

import '../plugins/util'

export default {
    name: 'app',
    data() {
        return {
            user_oauth: [{
                "id": 1,
                "app_name": "github",
                "image": "https://github.githubassets.com/favicons/favicon.png",
                "login_url": "https://github.com/login/oauth/authorize?client_id=01d5f5a68a65d1d2ef88&scope=user&redirect_uri=http%3A%2F%2Fwww.sheep.beer%2Flogin%3Fapp_name%3Dgithub",
                "help_text": "使用github登录",
                "client_id": "01d5f5a68a65d1d2ef88",
                "info": {"is_active": false}
            }, {
                "id": 2,
                "app_name": "weibo",
                "image": "https://open.weibo.com/favicon.ico",
                "login_url": "https://api.weibo.com/oauth2/authorize?client_id=3001368361&scope=all&redirect_uri=http%3A%2F%2F127.0.0.1%3A3000%2Flogin%3Fapp_name%3Dweibo",
                "help_text": "使用微博登录",
                "client_id": "3001368361",
                "info": {
                    "id": 2,
                    "created_time": "2020-10-19T14:43:12.230784",
                    "update_time": "2020-10-19T14:43:12.230823",
                    "is_active": true,
                    "app": 2,
                    "user": 23,
                    "uid": 6936210337,
                    "home_url": "https://www.weibo.com/u/6936210337"
                }
            }]
        }
    },
    methods: {},
    components: {},
    computed: {
        ...mapState(['user', 'option'])
    }
}
</script>
<style scoped lang="scss">
.applications {
    text-align: center;
    justify-content: space-around;
    margin-top: 12px;
    margin-left: 10px;
    display: inline-block;

    button {
        line-height: 1;
        min-width: 0;
        padding: 9px;
        border-radius: 50%;
        display: revert;
        width: revert;
        height: revert;
        color: revert;
        font-size: revert;
        cursor: pointer;

        .mat-button-wrapper {
            line-height: 1;
        }
    }

    button:active {
        background: #ecf5ff;
    }
}
</style>
