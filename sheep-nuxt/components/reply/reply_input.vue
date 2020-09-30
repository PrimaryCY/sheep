<template>
    <div class="create-reply">
        <a-comment>
            <a-avatar
                    slot="avatar"
                    :src="avatar"
                    alt="Han Solo"
            />
            <div slot="content">
                <tinymce-editor ref="tinymce"
                                v-model="html_content"
                                :height="160"
                                :menubar="false"
                                toolbar="reply_toolbar"
                                :statusbar="false"
                                :placeholder="placeholder"
                ></tinymce-editor>
                <el-button
                        class="reply-button"
                        size="mini"
                        :disabled="!html_content.trim().length"
                        @click="click_reply"
                        type="primary">
                    回复
                </el-button>
            </div>
        </a-comment>
    </div>
</template>

<script>
    import tinymceEditor from '@/components/Tinymce/tinymce-editor'

    export default {
        name: "reply_input",
        data() {
            return {
                html_content: ''
            }
        },
        props: {
            reply_name: {
                type: String,
                default: ''
            },
            avatar: {
                type: String,
                default: 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2519824424,1132423651&fm=26&gp=0.jpg'
            },
            post_id: {
                type: Number,
                required: true
            },
            parent_id: {
                type: Number,
                required: false
            }
        },
        methods: {
            click_reply() {
                // 回复
                let data = {
                    post_id:this.post_id,
                    html_content: this.html_content,
                    content:this.$refs['tinymce'].get_content()
                }
                if(this.parent_id)data['parent_id']=this.parent_id
                this.html_content = ""
                this.$emit("click_reply_btn", data)
            }
        },
        components: {
            tinymceEditor
        },
        computed: {
            placeholder() {
                return this.reply_name ? `回复 ${this.reply_name} :` : ''
            }
        }
    }
</script>

<style scoped lang="scss">
    .create-reply {
        text-align: right;
    }
</style>