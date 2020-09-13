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
            avatar:{
                type:String,
                default:'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2519824424,1132423651&fm=26&gp=0.jpg'
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
    .create-reply{
        text-align: right;
    }
</style>