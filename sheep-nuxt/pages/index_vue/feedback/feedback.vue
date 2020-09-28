<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
    <div class="feedback">
        <div class="feedback-header">
            <p class="header-img">
                <img src="@/static/img/feedback_title.jpg">
            </p>
            <div class="header-content">
                <p>
                    🎉感谢您使用sheep！请告诉我们您对sheep的意见和建议，
                </p>
                <p>
                    我们会参考您的反馈不断优化我们的产品和服务。
                </p>
            </div>

        </div>
        <div class="feedback-content">
            <el-tabs type="card" v-model="schema" @tab-click="change_schema">
                <el-tab-pane label="🔨提出意见" name="form">
                    <el-form label-width="80px" :model="form"
                             ref="fb_form"
                             :rules="rules"
                             label-position="top" size="mini">
                        <el-form-item label="问题类别:" size="mini" prop="category_id">
                            <el-radio-group v-model="form.category_id">
                                <el-radio v-for="c in feedback_category"
                                          :key="c.id"
                                          :label="c.id">
                                    {{c.name}}
                                </el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label-width="8px" prop="html_content">
                            <p>问题描述:</p>
                            <no-ssr placeholder="Loading...">
                                <tinymce-editor v-model="form.html_content"
                                                ref="tinymce"
                                                :height="340"
                                                :menubar="false"
                                                toolbar="simple_toolbar"
                                                placeholder="在这里请写下您宝贵的意见,我们会加油努力改进哒!"
                                ></tinymce-editor>
                            </no-ssr>
                        </el-form-item>
                        <el-form-item label="联系方式(注明一下是手机号/微信/qq号,方便我们联系):" prop="contact_way">
                            <el-input v-model="form.contact_way"></el-input>
                        </el-form-item>
                        <el-form-item size="large" style="text-align: center" label-width="0px">
                            <el-button @click="$refs['fb_form'].resetFields()">
                                重置
                            </el-button>
                            <el-button type="primary" @click="sumbit">
                                提交
                            </el-button>
                        </el-form-item>
                    </el-form>
                </el-tab-pane>
                <el-tab-pane v-if="user.is_anonymity" label="📃历史反馈" name="history">
                    <div class="check-box">
                        <el-checkbox v-model="params.has_reply" @change="_get_history_fb(false)">只看已回复</el-checkbox>
                    </div>
                    <list :list="feedbacks.results">
                        <template v-slot:item-content="data">
                            <div @click="open_dialog(data.item)">
                                <el-row>
                                    <el-col :span="10">
                                        <div class="history-title">
                                            <font_icon :type="data.item.reply_author_id?3:4"></font_icon>
                                            &nbsp;&nbsp;&nbsp;问题类别:{{_fb_category(data.item.category_id)}}
                                        </div>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col :span="22">
                                        <div class="three-line-ellipsis pointer">
                                            {{data.item.content}}
                                        </div>
                                    </el-col>
                                </el-row>
                            </div>
                        </template>
                    </list>
                    <div class="footer-pagination">
                        <pagination
                                @change="_get_history_fb"
                                :pagination_config="{layout:'total, sizes, prev, pager, next',background:true}"
                                :params="params"
                                :pager="feedbacks"></pagination>
                    </div>
                </el-tab-pane>
            </el-tabs>
        </div>

        <el-dialog title="反馈详情" :visible.sync="history_fb.flag"
                   :modal-append-to-body=false>
            <div class="dialog">
                <div class="dialog_title">
                    问题类别:{{_fb_category(history_fb.now_fb.category_id)}}
                </div>
                <div class="html_content" v-html="history_fb.now_fb.html_content"></div>
                <bubble_text
                        v-if="history_fb.now_fb.reply_author_id"
                        :text="history_fb.now_fb.reply"
                        :time="`回复时间:${history_fb.now_fb.reply_time}`"
                        position="right">
                    <template v-slot:user>
                        <div class="dialog_reply">
                            <img src="@/static/img/admin_portrait.jpg">
                            <span>{{`admin0${history_fb.now_fb.reply_author_id}`}}</span>
                        </div>
                    </template>
                </bubble_text>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    import {mapState} from 'vuex'

    import list from '@/components/list/list'
    import bubble_text from '@/components/common/bubble_text'
    import pagination from '@/components/pagination'
    import font_icon from '@/components/small/font_icon'
    import tinymceEditor from '../../../components/Tinymce/tinymce-editor'
    import {api_feedback_category, api_feedback} from '../../../api'

    export default {
        name: 'feedback',
        data() {
            return {
                visable: true,
                history_fb: {
                    now_fb: {}, //当前查看的feedback详情
                    flag: false,
                },
                schema: 'form',
                feedback_category: [],
                form: {
                    html_content: '',
                    content: '',
                    category_id: undefined,
                    contact_way: '',
                },
                rules: {
                    category: [{required: true, message: '你忘了选反馈类别了呢😋!', trigger: 'blur'}],
                    html_content: [{required: true, message: '你忘了输入问题详细内容呢😘!', trigger: 'blur'}],
                    contact_way: [
                        {required: true, message: '亲,留个微信号吧😙!', trigger: 'blur'},
                        {max: 30, message: '联系方式最多只能30个字符呢🙈', trigger: 'blur'}
                    ]
                },
                params: {
                    limit: 10,
                    offset: 0,
                    has_reply: false,
                },
                feedbacks: {
                    total: 0,
                    results: null
                }
            }
        },
        methods: {
            open_dialog(item) {
                this.history_fb.now_fb = item
                this.history_fb.flag = !this.history_fb.flag
            },
            change_schema() {
                if (this.schema === 'history') {
                    this._get_history_fb(false)
                }
            },
            _fb_category(id) {
                for (let c of this.feedback_category) {
                    if (c.id === id) {
                        return c.name
                    }
                }
            },
            async _get_category() {
                if (process.client) {
                    let res = await api_feedback_category.list()
                    res = res.data
                    if (res.code !== 2000) {
                        this.Message(res.msg)
                        return null
                    }
                    this.feedback_category = res.data
                }
            },
            async sumbit() {
                this.$refs['fb_form'].validate(async (valid) => {
                    if (!valid) {
                        return false
                    }
                    let loading = this.openLoading(
                        {
                            'text': '提交中',
                            'target': '.el-tabs__content',
                        }
                    )
                    this.form.content = this.$refs['tinymce'].get_content()
                    let res = await api_feedback.create(this.form)
                    res = res.data
                    if (res.code !== 2000) {
                        loading.close()
                        this.$message(res.msg)
                        return null
                    }
                    loading.close()
                    this.$message.success('提交成功,之后注意查看回复哦!')
                    this.schema = 'history'
                    this._get_history_fb()
                })
            },
            async _get_history_fb(move_to_top = true) {
                if (move_to_top) {
                    this.move_to_top()
                }
                let loading = this.openLoading({
                    target: '.el-tabs__content'
                })
                let res = await api_feedback.list(this.params)
                res = res.data
                loading.close()
                if (res.code !== 2000) {
                    this.$message(res.msg)
                    return null
                }
                this.feedbacks = res.data
            }
        },
        async created() {
            await this._get_category()
        },
        computed: {
            ...mapState(['user'])
        },
        components: {
            tinymceEditor,
            pagination,
            list,
            font_icon,
            bubble_text
            // textComponents
        },
        inject: ['move_to_top']
    }
</script>

<style scoped lang="scss">

    .feedback {
        .feedback-header {
            margin-bottom: 5px;

            .header-img {
                margin-bottom: 0;
                text-align: center;

                img {
                    width: 22%;
                    height: 22%;
                }
            }

            .header-content {
                background-color: #fffbec;
                color: #888;
                border-top: 1px #f6f1dc solid;
                padding: 11px 26px 11px 15px;

                p {
                    margin-bottom: 1px;
                }
            }
        }

        .feedback-content {
            margin: 0;
            padding: 0;
            text-align: initial;
            font-size: 18px;
        }
    }


    .check-box {
        text-align: right;
    }

    .history-title {
        font-size: 12px;
        font-weight: bold;
    }

    .dialog {
        .dialog_title {
            text-align: left;
            padding: 0 8px;
            font-weight: bold;
        }
        .html_content{
            /deep/ img{
                width: 100%;
            }
        }
        .dialog_reply {
            img {
                display: block;
            }

            span {
                font-size: 12px;
            }
        }
    }
</style>
