<template>
    <div class="login_wrapper">
        <no-ssr>
            <vue-particles
                    color="#000000"
                    :particleOpacity="0.9"
                    :particlesNumber="60"
                    shapeType="circle"
                    :particleSize="6"
                    linesColor="#000"
                    :linesWidth="1"
                    :lineLinked="true"
                    :lineOpacity="0.8"
                    :linesDistance="150"
                    :moveSpeed="3"
                    :hoverEffect="true"
                    hoverMode="repulse"
                    :clickEffect="true"
                    clickMode="push"
            >
            </vue-particles>
        </no-ssr>
        <div class="content" :class="{'s--signup':status === 'register'}">

            <!--			登录-->
            <div class="form sign-in">
                <h2>欢迎回来</h2>
                <label>
                    <span>邮箱</span>
                    <input type="text"
                           v-model="loginData.email_or_phone"
                           placeholder="请输入邮箱用户名"
                           @keyup="login_watch(1)"
                           maxlength="20"
                           minlength="3"/>
                    <p v-if="loginError.email_or_phone" class="error-msg"><a
                            href="javascript:">{{ loginError.email_or_phone }}</a>
                    </p>
                </label>
                <label>
                    <span>密码</span>
                    <input type="password"
                           v-model="loginData.password"
                           placeholder="请输入密码"
                           @keyup.enter="login"
                           @keyup="login_watch(2)" maxlength="20"/>
                    <p v-if="loginError.password" class="error-msg"><a href="javascript:">{{ loginError.password }}</a>
                    </p>
                    <el-checkbox v-model="loginData.remember_me">记住账户</el-checkbox>
                    <el-checkbox v-model="bind_user_flag" v-if="bind_user_flag" disabled>自动关联{{oauth_info.app_name}}用户</el-checkbox>
                </label>
                <br>
                <!--				<p class="forgot-pass"><a href="javascript:">忘记密码？</a></p>-->
                <button type="button" class="submit"
                        @click="login"
                        :class="{'submit_disable':loginError.flag}"
                        :disabled="loginError.flag"
                >登 录
                </button>

                <div class="applications">
                    <el-tooltip v-for="a in applications" :key="a.id"
                                effect="light"
                                :content="a.help_text"
                                placement="bottom">
                        <button
                                @click="push_application(a.login_url)"
                                type="button">
                        <span class="mat-button-wrapper">
                            <img :src="a.image"/>
                        </span>
                        </button>
                    </el-tooltip>

                </div>
            </div>
            <!--			注册-->
            <div class="sub-cont">
                <div class="img">
                    <div class="img__text m--up">
                        <h2 class="title">还未注册？</h2>
                        <p>立即注册，发现大量机会！</p>
                    </div>
                    <div class="img__text m--in">
                        <h2 class="title">已有帐号？</h2>
                        <p>有帐号就登录吧，好久不见了！</p>
                    </div>
                    <div class="img__btn">
                        <span class="m--up" @click="status='register'">注 册</span>
                        <span class="m--in" @click="status='login'">登 录</span>
                    </div>
                </div>
                <div class="form sign-up">
                    <h2>立即注册</h2>
                    <label>
                        <span>用户名</span>
                        <input type="text"
                               v-model="registerData.username"
                               placeholder="请输入用户昵称,不可修改"
                               @keyup="register_watch(1)"
                        />
                        <p v-if="registerError.username" class="error-msg"><a
                                href="javascript:">{{ registerError.username }}</a>
                        </p>
                    </label>
                    <label>
                        <span>邮箱</span>
                        <input type="email"
                               v-model="registerData.email"
                               placeholder="请输入注册邮箱,登录使用"
                               @keyup="register_watch(2)"
                        />
                        <p v-if="registerError.email" class="error-msg"><a
                                href="javascript:">{{ registerError.email }}</a></p>
                    </label>
                    <label>
                        <span>密码</span>
                        <input type="password"
                               v-model="registerData.password"
                               placeholder="请输入大于6位的密码"
                               @keyup="register_watch(3)"
                        />
                        <p v-if="registerError.password" class="error-msg"><a
                                href="javascript:">{{ registerError.password }}</a>
                        </p>
                    </label>
                    <label>
                        <span>重复输入密码</span>
                        <input type="password"
                               v-model="registerData.verify_password"
                               placeholder="请重复输入密码"
                               @keyup="register_watch(3)"
                        />
                        <p v-if="registerError.verify_password" class="error-msg"><a
                                href="javascript:">{{ registerError.verify_password }}</a>
                        </p>
                    </label>
                    <button type="button" class="submit"
                            :class="{'submit_disable':registerError.flag}"
                            :disabled="registerError.flag"
                            @click="register"
                    >注 册
                    </button>
                    <!--					<button type="button" class="fb-btn">使用 <span>facebook</span> 帐号注册</button>-->
                </div>
            </div>
            <div style="height: 100%; width: 100%; background-image: radial-gradient(at 45px 45px, rgb(0, 255, 255) 0%, rgba(0, 0, 255, 0) 50%, rgb(0, 0, 255) 95%); opacity: 0.18; position: absolute;"></div>

        </div>
        <el-dialog
                :visible.sync="oauth_dialog"
                width="30%"
                top="45vh"
                center
                :close-on-press-escape=false
                :close-on-click-modal=false
                :show-close=false
                :modal-append-to-body=false
        >
            <div class="oauth-content">
                <div class="oauth-text">
                    首次第三方登录用户需要选择绑定老用户或者直接登录!
                </div>
                <el-button
                        class="left-button"
                        @click="bind_user">绑定用户
                </el-button>
                <el-button
                        class="right-button"
                        type="primary" @click="oauth_login(2)">直接登录➡️
                </el-button>
            </div>
        </el-dialog>
    </div>

</template>

<script>
// import remote_js from '../../components/remote-js.js'
import re from '../../utils/re'
import setting from '../../conf/settings'
import {
    api_user,
    api_o_applications,
    api_login,
    api_o_token,
    api_o_register
} from '../../api'
// import {sleep} from "../../utils/util"

export default {
    name: "login",
    inject: ['reload'],
    data() {
        return {
            status: 'login',
            bind_user_flag:false,   // 绑定用户
            oauth_dialog: false,    // 第三方登录dialog框
            oauth_info: {
                key:'',
                app_name:null,
            },                      // 第三方登录随机码
            applications: [],
            loginData: {
                email_or_phone: '',
                password: '',
                remember_me: false,
            },
            loginError: {
                email_or_phone: '',
                password: "",
                flag: true
            },
            registerData: {
                username: '',
                email: '',
                password: '',
                verify_password: ''
            },
            registerError: {
                username: '',
                email: '',
                password: '',
                verify_password: '',
                flag: true
            }
        }
    },
    methods: {
        async oauth_login(t) {
            // t为1绑定用户
            // t为2直接登录
            let res = await api_o_register.create({t, k:this.oauth_info.k})
            res = res.data
            if(res.code !== 2000){
                return
            }

            if(t === 2){
                this._login(res.data.token)
            }
        },
        bind_user() {
            this.bind_user_flag = true
            this.oauth_dialog = false
        },
        async oauth_auto_login() {
            // 第三方自动登录
            if (this.$route.query.code && this.$route.query.app_name) {
                let oauth = {
                    code: this.$route.query.code,
                    app_name: this.$route.query.app_name
                }
                let res = await api_o_token.create(oauth)
                res = res.data
                if (res.code !== 2000) {
                    return this.$message(res.msg)
                } else if (res.data.type === 1) {
                    // 用户已绑定第三方账号
                    this._login(res.data.token)
                } else if (res.data.type === 2) {
                    // 用户未绑定，弹出提示框让用户选择
                    this.oauth_dialog = true
                    this.oauth_info = res.data
                }
            }
        },
        push_application(url) {
            window.location.href = url
        },
        auto_input_email_or_phone() {
            // 自动输入用户名
            this.loginData.email_or_phone = this.$cookies.secure_get('un')
            if (this.loginData.email_or_phone) {
                this.loginData.remember_me = true
            }
        },
        async login() {
            let data = this.loginData
            const loading = this.openLoading({
                'text': '登陆中',
                'target': '.form'
            })
            // let res = await post_login(data)
            let res = await api_login.create(data)
            res = res.data
            if (res.code === 2000) {
                this._login(res.data.token, async ()=>{
                    this._save_remeber_me(res.data)
                    if (this.bind_user_flag){
                        await this.oauth_login(1)
                    }
                })
            } else if (res.msg.indexOf('邮箱') !== -1) {
                this.loginError.email_or_phone = res.msg
            } else if (res.msg.indexOf('密码') !== -1) {
                this.loginError.password = res.msg
            }
            this.loginError.flag = true
            loading.close()
        },
        _login(token, after_login){
            this.$cookies.secure_set(setting.TOKEN_NAME, token, {maxAge: setting.TOKEN_EXPIRE})
            // 如果之前已经登录其它账号,先清空再获取新用户信息
            this.$store.dispatch('modify_userinfo', {})
            this.$store.dispatch('receive_userinfo')
            after_login && after_login()
            this.$router.replace(this.$route.query.from || {'name': 'index'})
        },
        _save_remeber_me(data){
            if (this.loginData.remember_me) {
                this.$cookies.secure_set('un', data.email_or_phone, {maxAge: this.$settings.TOKEN_EXPIRE})
            }
        },
        login_watch(num) {
            //	监听数据变化, 1为用户名 2为密码
            let err = ''
            let email_or_phone = this.loginData.email_or_phone
            let pwd = this.loginData.password
            if (num === 1) {
                if (email_or_phone.length === 0) {
                    //	empty
                } else if (email_or_phone.length < 6) {
                    err = '邮箱或手机号不正确!'
                } else if (!re.phone.test(email_or_phone) && !re.email.test(email_or_phone)) {
                    err = '邮箱或手机号码格式不正确!'
                }
                this.loginError.email_or_phone = err
            } else {
                if (pwd.length === 0) {
                    // empty
                } else if (pwd.length < 6) {
                    err = '密码不正确!'
                }
                this.loginError.password = err
            }
            //控制登录按钮是否可用
            this.loginError.flag = !((!this.loginError.password && !this.loginError.email_or_phone) && (
                    pwd.length !== 0 && email_or_phone.length !== 0
            ))
        },
        // 注册相关
        async register() {
            const loading = this.openLoading({
                'text': '注册中',
                'target': '.form.sign-up'
            })
            let data = {...this.registerData}
            delete data.verify_password
            let res = await api_user.create(data)
            res = res.data
            if (res.code === 2000) {
                this.$message({
                    message: '恭喜你，注册成功,请登录!',
                    type: 'success'
                })
                this.loginData.email_or_phone = res.data.email
                this.registerData = {}
                this.status = 'login'
            } else if (res.msg.indexOf('用户') !== -1) {
                this.registerError.username = res.data.msg
            } else if (res.msg.indexOf('密码') !== -1) {
                this.registerError.password = res.data.msg
            } else if (res.msg.indexOf('邮箱') !== -1) {
                this.registerError.email = res.data.msg
            } else {
                this.$message(res.data.msg)
            }

            this.registerError.flag = true
            loading.close()
        },
        register_watch(num) {
            //	监听注册数据变化 1:用户名 2:邮箱 3:密码,重复输入密码
            let err = ''
            let {username, email, password, verify_password} = this.registerData
            switch (num) {
                case 1:
                    if (username.length === 0) err = ''
                    else if (re.special_str.test(username)) {
                        let s = username.match(re.special_str)
                        err = `用户名中出现了非法字符 "${s}"!`
                    }
                    this.registerError.username = err
                    break
                case 2:
                    if (email.length === 0) err = ''
                    else if (!re.email.test(email)) {
                        err = '邮箱格式不正确!'
                    }
                    this.registerError.email = err
                    break
                case 3:
                    if (password.length === 0) err = ''
                    else if (password.length < 6) {
                        err = '请输入大于六位的密码!'
                    }else if(re.space.test(password)){
                        err = '密码中不能包含空格!'
                    }

                    this.registerError.password = err
                    if (verify_password.length === 0) err = ''
                    if (verify_password !== password) {
                        err = '两次密码输入不一致!'
                    }
                    this.registerError.verify_password = err
            }

            //控制注册按钮是否可用
            this.registerError.flag = !((!this.registerError.password
                    && !this.registerError.verify_password
                    && !this.registerError.email
                    && !this.registerError.username
            ) && (
                    password.length !== 0
                    && username.length !== 0
                    && verify_password.length !== 0
                    && email.length !== 0
            ))
        }
    },
    async asyncData(context) {
        try {
            let applications
            let res = {
                'applications': [],
            }
            let async_list = [
                api_o_applications.list()
            ];
            [applications] = await Promise.all(async_list)
            res.applications = applications.data.data
            return res
        } catch (e) {
            context.error({statusCode: 500, message: 'ssr internal server error'})
        }
    },
    // components: {
    // 	remote_js
    // }
    beforeCreate() {
        if (process.client) {
            history.replaceState(null, null, '/login')
        }
    },
    created() {
        // 打开页面读取记住用户数据
        if (process.client) {
            this.oauth_auto_login()
            this.auto_input_email_or_phone()
        }
    },
}
</script>

<style scoped lang="scss">
//*, *:before, *:after {
//    box-sizing: border-box;
//    margin: 0;
//    padding: 0;
//}

/deep/ .el-dialog {
    border-radius: 15px !important;

    .el-dialog__header {
        padding: 0;
    }

    .oauth-content {
        text-align: center;

        .oauth-text {
            margin: 20px;
        }

        button {
            display: inline-block;
            height: revert;
        }

        .left-button {
            display: inline-block;
            line-height: 1;
            white-space: nowrap;
            cursor: pointer;
            background: #FFF;
            border: 1px solid #DCDFE6;
            color: #606266;
            -webkit-appearance: none;
            text-align: center;
            box-sizing: border-box;
            margin: 0;
            transition: .1s;
            font-weight: 500;
            padding: 12px 20px;
            font-size: 14px;
        }

        .left-button:hover {
            color: #364045;
            border-color: rgb(195, 198, 199);
            background-color: rgb(235, 236, 236);
        }

        .right-button {
            display: inline-block;
            line-height: 1;
            white-space: nowrap;
            cursor: pointer;
            -webkit-appearance: none;
            text-align: center;
            box-sizing: border-box;
            margin: 0;
            transition: .1s;
            font-weight: 500;
            padding: 12px 20px;
            font-size: 14px;
            color: #FFF;
            background-color: #364045;
            border-color: #364045;
        }

        .right-button:hover {
            background: rgb(94, 102, 106);
            border-color: rgb(94, 102, 106);
            color: #FFF;
        }
    }

}

/*
第三方应用
 */
.applications {
    text-align: center;
    justify-content: space-around;
    margin-top: 12px;

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

body {
    font-family: 'Open Sans', Helvetica, Arial, sans-serif;
    background: #ededed;
}

input, button {
    border: none;
    outline: none;
    background: none;
    font-family: 'Open Sans', Helvetica, Arial, sans-serif;
}

.tip {
    font-size: 20px;
    margin: 40px auto 50px;
    text-align: center;
}

.content {
    /*以中心缩放*/
    -webkit-transform: scale(.8, .8);
    opacity: 0.9;
    border-radius: 3%;
    overflow: hidden;
    position: absolute;
    left: 50%;
    top: 50%;
    width: 900px;
    height: 550px;
    margin: -300px 0 0 -450px;
    background: #fff;
}

.form {
    position: relative;
    width: 640px;
    height: 100%;
    transition: -webkit-transform 0.6s ease-in-out;
    transition: transform 0.6s ease-in-out;
    transition: transform 0.6s ease-in-out, -webkit-transform 0.6s ease-in-out;
    padding: 50px 30px 0;
}

.sub-cont {
    overflow: hidden;
    position: absolute;
    left: 640px;
    top: 0;
    width: 900px;
    height: 100%;
    padding-left: 260px;
    background: #fff;
    transition: -webkit-transform 0.6s ease-in-out;
    transition: transform 0.6s ease-in-out;
    transition: transform 0.6s ease-in-out, -webkit-transform 0.6s ease-in-out;
}

.content.s--signup .sub-cont {
    -webkit-transform: translate3d(-640px, 0, 0);
    transform: translate3d(-640px, 0, 0);
}

button {
    display: block;
    margin: 0 auto;
    width: 260px;
    height: 36px;
    border-radius: 30px;
    color: #fff;
    font-size: 15px;
    cursor: pointer;
}

button:active {
    background: #a11663;
}

.img {
    overflow: hidden;
    z-index: 2;
    position: absolute;
    left: 0;
    top: 0;
    width: 260px;
    height: 100%;
    padding-top: 360px;
}

.img:before {
    content: '';
    position: absolute;
    right: 0;
    top: 0;
    width: 900px;
    height: 100%;
    background-image: url(../../static/img/bg.jpg);
    background-size: cover;
    transition: -webkit-transform 0.6s ease-in-out;
    transition: transform 0.6s ease-in-out;
    transition: transform 0.6s ease-in-out, -webkit-transform 0.6s ease-in-out;
}

.img:after {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
}

.content.s--signup .img:before {
    -webkit-transform: translate3d(640px, 0, 0);
    transform: translate3d(640px, 0, 0);
}

.img__text {
    z-index: 2;
    position: absolute;
    left: 0;
    top: 50px;
    width: 100%;
    padding: 0 20px;
    text-align: center;
    color: #fff;
    transition: -webkit-transform 0.6s ease-in-out;
    transition: transform 0.6s ease-in-out;
    transition: transform 0.6s ease-in-out, -webkit-transform 0.6s ease-in-out;
}

.img__text h2 {
    margin-bottom: 10px;
    font-weight: normal;
}

.img__text p {
    font-size: 14px;
    line-height: 1.5;
}

.content.s--signup .img__text.m--up {
    -webkit-transform: translateX(520px);
    transform: translateX(520px);
}

.img__text.m--in {
    -webkit-transform: translateX(-520px);
    transform: translateX(-520px);
}

.content.s--signup .img__text.m--in {
    -webkit-transform: translateX(0);
    transform: translateX(0);
}

.img__btn {
    overflow: hidden;
    z-index: 2;
    position: relative;
    width: 100px;
    height: 36px;
    margin: 0 auto;
    background: transparent;
    color: #fff;
    text-transform: uppercase;
    font-size: 15px;
    cursor: pointer;
}

.img__btn:after {
    content: '';
    z-index: 2;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    border: 2px solid #fff;
    border-radius: 30px;
}

.img__btn span {
    position: absolute;
    left: 0;
    top: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    transition: -webkit-transform 0.6s;
    transition: transform 0.6s;
    transition: transform 0.6s, -webkit-transform 0.6s;
}

.img__btn span.m--in {
    -webkit-transform: translateY(-72px);
    transform: translateY(-72px);
}

.content.s--signup .img__btn span.m--in {
    -webkit-transform: translateY(0);
    transform: translateY(0);
}

.content.s--signup .img__btn span.m--up {
    -webkit-transform: translateY(72px);
    transform: translateY(72px);
}

h2 {
    width: 100%;
    font-size: 26px;
    text-align: center;
}

label {
    display: block;
    width: 260px;
    margin: 25px auto 0;
    text-align: center;
}

label span {
    font-size: 12px;
    color: #909399;
    text-transform: uppercase;
}

input {
    display: block;
    width: 100%;
    margin-top: 5px;
    padding-bottom: 5px;
    font-size: 16px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.4);
    text-align: center;
}

.forgot-pass {
    margin-top: 15px;
    text-align: center;
    font-size: 12px;
    color: #cfcfcf;
}

.forgot-pass a {
    color: #cfcfcf;
}

.submit {
    margin-top: 40px;
    margin-bottom: 20px;
    text-transform: uppercase;
    background: #c94663;
}

.submit_disable {
    background: #A9A9A9;
    cursor: not-allowed;
}

.fb-btn {
    border: 2px solid #d3dae9;
    color: #8fa1c7;
}

.fb-btn span {
    font-weight: bold;
    color: #455a81;
}

.sign-in {
    transition-timing-function: ease-out;
}

.content.s--signup .sign-in {
    transition-timing-function: ease-in-out;
    transition-duration: 0.6s;
    -webkit-transform: translate3d(640px, 0, 0);
    transform: translate3d(640px, 0, 0);
}

.sign-up {
    -webkit-transform: translate3d(-900px, 0, 0);
    transform: translate3d(-900px, 0, 0);

    label {
        margin: 12px auto 0 !important;

        input {
            margin-top: 0 !important;
        }
    }
}

.content.s--signup .sign-up {
    -webkit-transform: translate3d(0, 0, 0);
    transform: translate3d(0, 0, 0);
}

.m--up, .m--in {
    z-index: 9999 !important;
}

.title {
    color: #c94663;
}

.error-msg {
    color: #d20505;
    font-size: 15px;
}
</style>
