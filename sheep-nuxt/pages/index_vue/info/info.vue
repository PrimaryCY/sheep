<template>
    <!--	<div v-if="user.portrait">-->
    <div>
        <div class="container">
            <!--			用户头像-->
            <div class="avatar" v-cloak>
                <el-row align="bottom" type="flex">
                    <el-col :span="5" :offset="4">
                        <div class="block">
                            <el-avatar :size="120" :src="reader_portrait">
                                <img :src="reader_portrait"/>
                            </el-avatar>
                        </div>
                    </el-col>
                    <el-col :span="4">
                        <el-avatar :size="80" :src="reader_portrait">
                            <img :src="reader_portrait"/>
                        </el-avatar>
                    </el-col>
                    <el-col :span="3">
                        <el-avatar :size="60" :src="reader_portrait">
                            <img :src="reader_portrait"/>
                        </el-avatar>
                    </el-col>
                    <el-col :span="2">
                        <el-avatar :size="40" :src="reader_portrait">
                            <img :src="reader_portrait"/>
                        </el-avatar>
                    </el-col>
                    <el-col :span="3" :offset="3">
                        <el-upload
                                :show-file-list="false"
                                action=""
                                :before-upload="before_avatar_upload">
                            <el-button plain
                                       type="info"
                                       size="mini"
                                       round>
                                更换头像
                            </el-button>
                        </el-upload>
                        <el-button plain
                                   type="primary"
                                   v-if="uploadData.flag"
                                   size="mini"
                                   round
                                   :class="'submit_portrait'"
                                   @click="upload_portrait"
                        >确定更换
                        </el-button>
                    </el-col>
                </el-row>
            </div>
            <!--			用户资料-->
            <el-main class="user">
                <el-row :gutter="1">
                    <el-col :span="22">
                        <svg v-if="user.gender===0" class="icon-min" aria-hidden="true">
                            <use xlink:href="#icon-xingbienv-copy"></use>
                        </svg>
                        <svg v-else class="icon-min" aria-hidden="true">
                            <use xlink:href="#icon-xingbienan-copy"></use>
                        </svg>
                        :
                        <span class="name">{{ user.username }}</span>

                        <div class="applications">

                            <button
                                    v-for="a in this.user_oauth" :key="a.id"
                                    @click="blank_window_push(a.info.home_url)"
                            >
                                        <span class="mat-button-wrapper">
                                            <img :src="a.image"/>
                                        </span>
                            </button>

                        </div>

                    </el-col>
                </el-row>
                <br>
                <el-row type="flex" align="bottom">
                    <el-col :span="5">
                        <svg class="icon-min" aria-hidden="true">
                            <use xlink:href="#icon-youxiang-"></use>
                        </svg>
                        :
                        {{ user.email ? user.email : '暂未绑邮箱' }}
                    </el-col>
                    <el-col :span="4" :offset="1">
                        <svg class="icon-min" aria-hidden="true">
                            <use xlink:href="#icon-shouji-"></use>
                        </svg>
                        :
                        {{ user.phone ? user.phone : '暂未绑定手机号' }}
                    </el-col>

                </el-row>

            </el-main>

        </div>

        <div class="info">
            <el-tabs class="space" type="card" :stretch="true">
                <el-tab-pane label="📅动态">
                    <dynamic :results="user_dynamic.results"></dynamic>
                    <div v-show="user_dynamic.next" class="loading">
                        <el-button
                                style="width: 15%;margin-top: 20px"
                                v-show="user_dynamic_params.offset < user_dynamic.count"
                                :loading="user_dynamic_loading"
                                @click="get_user_dynamic">
                            查看更多>>
                        </el-button>
                    </div>
                </el-tab-pane>
                <!--			用户信息修改-->
                <el-tab-pane label="📃个人资料" class="data">
                    <el-row type="flex">
                        <el-col :span="3" :offset="21">
                            <el-button plain size="small" type="info" @click="edit.flag=!edit.flag">
                                修改资料
                                <svg class="icon-min" aria-hidden="true">
                                    <use xlink:href="#icon-shezhi"></use>
                                </svg>
                            </el-button>
                        </el-col>
                    </el-row>
                    <el-form label-width="100px"
                             ref="rule_edit"
                             :model="edit"
                             :rules="rules"
                             label-position="'left"
                    >
                        <el-form-item label="用户名:" prop="name">
                            <el-input :placeholder="user.username" disabled></el-input>
                        </el-form-item>
                        <el-form-item label="邮箱:" prop="email">
                            <el-input :placeholder="user.email" disabled></el-input>
                        </el-form-item>
                        <el-form-item label="手机号:" prop="phone">
                            <el-input v-if="user.is_phone"
                                      v-model="edit.phone"
                                      disabled></el-input>
                            <el-input v-else
                                      v-model="edit.phone"
                                      placeholder="请输入手机号"
                                      :disabled="!edit.flag"></el-input>
                        </el-form-item>
                        <el-form-item label="生日:">
                            <el-col :span="11">
                                <el-form-item prop="birth">
                                    <el-date-picker type="date"
                                                    v-model="edit.birth"
                                                    style="width: 100%;"
                                                    value-format="yyyy-MM-dd"
                                                    placeholder="请输入生日"
                                                    :picker-options="pickerOptions"
                                                    :disabled="!edit.flag"></el-date-picker>
                                </el-form-item>
                            </el-col>
                            <el-col class="line" :span="2">-</el-col>
                        </el-form-item>
                        <el-form-item label="性别:" prop="gender">
                            <el-radio-group
                                    v-model="edit.gender"
                                    :disabled="!edit.flag">
                                <el-radio :label="1">男</el-radio>
                                <el-radio :label="0">女</el-radio>
                                <el-radio :label="2">保密</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="个人简介:" prop="brief">
                            <el-input type="textarea"
                                      v-model="edit.brief"
                                      :maxlength="200"
                                      show-word-limit
                                      :rows="7"
                                      :disabled="!edit.flag"
                                      placeholder="写一段短短的文字,简单介绍一下自己吧!"
                            ></el-input>
                        </el-form-item>
                        <el-form-item class="submit" v-if="edit.flag">
                            <el-button type="primary" @click="modify_info">提交修改</el-button>
                            <el-button @click="reset_info">重置</el-button>
                        </el-form-item>
                    </el-form>
                </el-tab-pane>
                <!--            用户密码修改-->
                <el-tab-pane label="🔑修改密码">
                    <change_pwd></change_pwd>
                </el-tab-pane>
                <el-tab-pane label="➕我的关注">
                    <focus schema="focus"
                           :data="user_focus">
                    </focus>
                </el-tab-pane>
                <el-tab-pane label="🌹我的粉丝">
                    <focus schema="fans"
                           :data="user_fans">
                    </focus>
                </el-tab-pane>
            </el-tabs>

        </div>

    </div>
</template>

<script>
import {mapState} from 'vuex'

import change_pwd from '@/components/form/change-pwd'
import dynamic from "@/components/dynamic/dynamic"
import focus from '@/components/focus/focus'
import {
    api_o_user_oauth,
    api_user_focus,
    api_upload,
    api_user, api_dynamic
} from "../../../api"
import re from '../../../utils/re'

export default {
    name: "info",
    head() {
        return {
            title: '个人中心',
        }
    },
    data() {
        return {
            user_dynamic:{
                results:[]
            },
            user_dynamic_params: {
                offset:0,
                limit: 3
            },
            user_dynamic_loading:false,
            user_fans: [],
            user_focus: [],
            user_oauth: [],  // 用户oauth信息
            uploadData: {
                // 上传图片的数据
                upload_path: 'sheep-portrait',
                file: undefined,
                flag: false
            },
            pickerOptions: { // 计费日期的约束条件
                disabledDate: this.validate_birth,
            },
            reader_portrait: this.$store.state.user.portrait,
            edit: {
                portrait: this.deepCopy(this.$store.state.user.portrait),
                phone: this.deepCopy(this.$store.state.user.phone),
                gender: this.deepCopy(this.$store.state.user.gender),
                birth: this.deepCopy(this.$store.state.user.birth),
                brief: this.deepCopy(this.$store.state.user.brief),
                flag: false,
            },
            rules: {
                phone: [
                    {
                        validator: this.validate_phone, trigger: 'change'//触发条件：blur、change
                    }],
                gender: [
                    {
                        required: true, message: '请选择性别!', trigger: 'blur'
                    }
                ]
            },
            ruleForm: {
                pass: '',
                checkPass: '',
                age: ''
            },

        }
    },
    computed: {
        ...mapState(['user'])
    },
    watch: {
        "user": {
            deep: true,
            handler: function (new_val) {
                this.edit = Object.assign(this.edit, new_val)
                this.reader_portrait = this.edit.portrait
            }
        }
    },
    methods: {
        async _get_user_focus() {
            // 获取当前用户的关注
            let res = await api_user_focus.list({type: 1})
            res = res.data
            if (res.code !== 2000) {
                return this.$message(res.msg)
            }
            this.user_focus = res.data
        },
        async _get_user_fans() {
            // 获取当前用户的粉丝
            let res = await api_user_focus.list({type: 2})
            res = res.data
            if (res.code !== 2000) {
                return this.$message(res.msg)
            }
            this.user_fans = res.data
        },
        async _get_user_oauth_info() {
            // 获取当前用户的第三方信息
            let res = await api_o_user_oauth.list()
            res = res.data
            if (res.code !== 2000) {
                return this.$message(res.msg)
            }
            this.user_oauth = res.data.filter(i => i.info.is_active)
        },
        validate_phone(r, v, callback) {
            // 验证用户输入的手机号
            if (v === null) {
                callback()
            } else if (!re.phone.test(v)) {
                callback(new Error("手机号码不正确!"))
            } else {
                callback()
            }
        },
        validate_birth(time) {
            // 验证用户生日
            return time.getTime() > Date.now() - 8.64e7
        },
        reset_info() {
            // 重置数据
            this.$refs['rule_edit'].resetFields()
        },
        modify_info() {
            // 修改个人资料
            this.$refs['rule_edit'].validate(async (valid) => {
                if (!valid) {
                    return false
                }
                let loading = this.openLoading(
                        {
                            'text': '修改中',
                            'target': '.el-tabs__content',
                        }
                )
                let res = await api_user.update(null, this.edit)
                if (res.data.code !== 2000) {
                    this.$message(res.data.msg)
                    loading.close()
                    return false
                }
                this.$store.dispatch('modify_userinfo', res.data.data)
                this.edit.flag = !this.edit.flag
                this.$message.success('修改成功!')
                loading.close()
            })
        },
        async upload_portrait() {
            // 上传修改头像
            let loading = this.openLoading({
                text: '上传中...',
                target: '#content-inner'
            })
            let portrait_res = await api_upload.upload(this.uploadData)
            if (portrait_res.data.code !== 2000) {
                this.$message('上传失败!请重试!')
                loading.close()
                return
            }
            this.edit.portrait = portrait_res.data.data.url
            let user_res = await api_user.partial_update(null, this.edit)
            if (user_res.data.code !== 2000) {
                this.$message(user_res.data.msg)
                loading.close()
                return
            }
            this.uploadData.flag = !this.uploadData.flag
            this.$store.dispatch('modify_userinfo', user_res.data.data)
            this.$message.success('修改成功!')
            loading.close()
        },
        before_avatar_upload(file) {
            const isJPG = file.type === "image/jpeg"
            const isPNG = file.type === "image/png"
            const isLt1M = file.size / 1024 / 1024 < 1

            if (!isJPG && !isPNG) {
                this.$message.error("上传头像图片只能是 JPG 或 PNG 格式!")
            } else if (!isLt1M) {
                this.$message.error("上传头像图片大小不能超过 1MB!")
            } else {
                this.uploadData.file = file
                this._image_preview(file)
                this.uploadData.flag = true
            }
            // 不使用upload自带的上传方式，而是使用axios，所以阻止upload自带的上传
            return false
        },
        _image_preview: function (file) {
            // 图片预览
            var self = this
            //定义一个文件阅读器
            var reader = new FileReader()
            //文件装载后将其显示在图片预览里
            reader.onload = function (e) {
                //将bade64位图片保存至数组里供上面图片显示
                self.reader_portrait = e.target.result
            }
            reader.readAsDataURL(file)
        },
        async get_user_dynamic(){
            this.user_dynamic_loading = true
            this.user_dynamic_params.offset += this.user_dynamic_params.limit
            await this._get_user_dynamic()
            this.user_dynamic_loading = false
        },
        async _get_user_dynamic(){
            // 获取用户动态
            let res = await api_dynamic.list(this.user_dynamic_params)
            res = res.data
            if (res.code !== 2000) {
                return this.$message(res.msg)
            }
            this.user_dynamic.count = res.data.count
            this.user_dynamic.next = res.data.next
            this.user_dynamic.results.push.apply(this.user_dynamic.results, res.data.results)

        }
    },
    components: {
        change_pwd,
        focus,
        dynamic
    },
    created() {
        if (process.server) {
            return
        }
        this._get_user_oauth_info()
        this._get_user_fans()
        this._get_user_focus()
        this._get_user_dynamic()
    },
    inject: ['blank_window_push']
}
</script>

<style scoped lang="scss">


#content {
    margin-left: 0;
}

.container {
    text-align: left;

    .avatar {
        text-align: center;

        .el-row:last-child {
            .submit_portrait {
                margin: 10px;
            }
        }
    }

    .user {
        margin-top: 20px;

        .name {
            font-size: 16px;
            font-weight: 700;
            color: #222;
        }

        .applications {
            text-align: center;
            justify-content: space-around;
            margin-left: 10px;
            display: inline-block;

            button {
                line-height: 1;
                min-width: 0;
                padding: 5px;
                border-radius: 50%;
                background-color: transparent;
                border: 0;
                display: revert;
                width: revert;
                height: revert;
                color: revert;
                font-size: revert;
                cursor: pointer;
                outline: none;

                .mat-button-wrapper {
                    line-height: 1;
                }

                img {
                    width: 23px;
                    height: 23px;
                    vertical-align: text-bottom;
                }
            }

            button:active {
                background: #ecf5ff;
            }
        }
    }
}

.info {
    .data {
        .el-form-item {
            text-align: left;
        }

        .el-row {
            margin-bottom: 15px;
        }

        .submit {
            text-align: center;
        }
    }
}

</style>
