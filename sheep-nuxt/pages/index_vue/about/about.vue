<template>
    <main>
        <div v-html="content" class="html-content">

        </div>
    </main>
</template>

<script>
import {api_about} from "@/api"

export default {
    name: "about",
    head () {
        return {
            title: '关于我们',
        }
    },
    data() {
        return {
            content: {}
        }
    },
    async asyncData(context) {
        try {
            let content
            let async_list = [
                api_about.list()
            ];
            [content] = await Promise.all(async_list)
            return {
                content: content.data.data
            }
        } catch (e) {
            context.error({statusCode: 500, message: 'ssr internal server error'})
        }
    },
}
</script>

<style scoped lang="scss">
#iframe {
    width: 100%;
    height: 100%
}
</style>