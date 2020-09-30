<template>
    <div v-if="type===2" class="base article-question-type">
        <svg class="icon-min" aria-hidden="true">
            <use xlink:href="#icon-wenti--copy"></use>
        </svg>
        <span>问题</span>
    </div>
    <div v-else-if="type===1" class="base article-post-type">
        <svg class="icon-min" aria-hidden="true">
            <use xlink:href="#icon-shiyongwendang"></use>
        </svg>
        <span>文章</span>
    </div>
    <div v-else-if="type===3" class="base feedback-replied">
        <svg v-cloak class="icon-min" aria-hidden="true">
            <use xlink:href="#icon-shiyongwendang"></use>
        </svg>
        <span>已回复</span>
    </div>
    <div v-else-if="type===4" class="base feedback-no-reply">
        <svg class="icon-min" aria-hidden="true">
            <use xlink:href="#icon-shiyongwendang"></use>
        </svg>
        <span>未回复</span>
    </div>
    <div v-else-if="type===5" class="base visible">
        <svg class="icon-min" aria-hidden="true">
            <use xlink:href="#icon-like-visable-copy"></use>
        </svg>
        <span>公开</span>
    </div>
    <div v-else-if="type===6" class="base disabled">
        <svg class="icon-min" aria-hidden="true">
            <use xlink:href="#icon-like-disable-copy"></use>
        </svg>
        <span>私密</span>
    </div>
    <div v-else-if="type===7" class="base disabled">
        <svg class="icon-min" aria-hidden="true">
            <use xlink:href="#icon-like-disable-copy"></use>
        </svg>
        <span>已读</span>
    </div>
    <div v-else-if="type===8" class="base disabled">
        <svg class="icon-min" aria-hidden="true">
            <use xlink:href="#icon-like-disable-copy"></use>
        </svg>
        <span>未读</span>
    </div>
</template>

<script>
export default {
    name: "post_type",
    props: {
        type: {
            type: Number,
            required: true
        }
    }
}
</script>

<style scoped lang="scss">
.base {
    display: inline;
    border-radius: 25%;
    width: 7%;
    height: 7%;
    text-align: center;
    font-size: 10px;
    color: white;
    opacity: .7;
    margin: 0 5px 0 0;
    padding: 4px;
    font-weight: normal;
}

.article-question-type {
    background-color: #b02727;
}

.article-post-type {
    background-color: #795548;
}

.feedback-replied {
    background-color: #364050;
    font-size: 10.5px;
}

.feedback-no-reply {
    background-color: #b02727;
    font-size: 10.5px;
}

.visible {
    font-size: 9px;
    padding: 3px;
    background-color: #b02727;
}

.disabled {
    font-size: 9px;
    padding: 3px;
    background-color: #364050;
}

</style>
