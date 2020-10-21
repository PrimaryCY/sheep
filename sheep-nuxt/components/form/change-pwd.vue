<template>
    <div class="pwd-wrap">
        <div class="pwd-content">
            <el-form :model="form"
                     status-icon
                     :rules="rules"
                     ref="ruleForm"
                     label-width="100px">
                <el-form-item
                        label="旧密码"
                        placeholder="请输入旧密码"
                        prop="r_p">
                    <el-input
                            v-model="form.r_p"
                            type="password"
                            autocomplete="off"
                    ></el-input>
                </el-form-item>
                <el-form-item
                        label="新密码"
                        prop="n_p">
                    <el-input type="password"
                              v-model="form.n_p"
                              autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item
                        label="确认密码"
                        prop="c_p">
                    <el-input type="password"
                              v-model="form.c_p"
                              autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                    <el-button @click="resetForm('ruleForm')">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>

</template>

<script>
import re from '../../utils/re'
import {api_pwd} from "@/api"


export default {
    name: "change-pwd",
    data() {
        let validate_r_p = (rule, value, callback) => {
           if(value.length < 6){
                return callback(new Error('密码不正确'));
            }
            return  callback()
        };
        let validate_n_p = (rule, value, callback) => {
            this.$refs.ruleForm.validateField('checkPass')
            callback()
        }
        let validate_c_p = (rule, value, callback) => {
            if(value.length < 6){
                return callback(new Error('新密码长度应大于6位数'));
            } else if (value !== this.form.n_p) {
                callback(new Error('两次输入密码不一致!'))
            } else if(re.space.test(value)){
                callback(new Error('密码中不能包含空格!'))
            }else if(value === this.form.r_p) {
                callback(new Error('新密码与旧密码相同'))
            }else {
                callback()
            }
        }
        return {
            form: {
                n_p: '',
                c_p: '',
                r_p: ''
            },
            rules: {
                n_p: [
                    {required: true, message: '新密码不能为空', trigger: 'blur'},
                    {validator: validate_n_p, trigger: 'blur'},
                ],
                c_p: [
                    {required: true, message: '新密码不能为空', trigger: 'blur'},
                    {validator: validate_c_p, trigger: 'blur'},
                ],
                r_p: [
                    {required: true, message: '请输入当前密码', trigger: 'blur'},
                    { validator: validate_r_p, trigger: 'blur' },
                ]
            }
        }
    }
    ,
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate(async (valid) => {
                if (!valid) {return false}
                let loading = this.openLoading({
                    text:'提交中...',
                    target: '.pwd-wrap',
                })
                let data = this.deepCopy(this.form)
                let res = await api_pwd.create(data)
                res = res.data
                if(res.code !== 2000){
                    loading.close()
                    return this.$message(res.msg)
                }
                this.form = {}
                loading.close()
                this.$message.success('修改成功！')
            })
        }
        ,
        resetForm(formName) {
            this.$refs[formName].resetFields()
        }
    }
}
</script>

<style scoped lang="scss">
.pwd-wrap{
    padding: 30px 0;
    width: 100%;
    text-align: center;
    .pwd-content{
        display: inline-block;
        width: 60%;
    }
}
</style>