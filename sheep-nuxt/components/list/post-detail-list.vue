<template>
    <div class="list">
        <div class="title" v-if="title && list.length !== 0">
            {{title}}
        </div>
        <a
                v-for="(i, index) in list"
                :key="i.id"
                :href="$router.resolve({name:'post_detail',params:{id:i.id}}).href"
                target="_blank"
                :class="{need_bottom:bottom}"
                class="sidebar-list-item">
            <slot name="item-content" :item="i" :index="index">

            </slot>
        </a>
    </div>
</template>

<script>
    export default {
        name: 'post-detail-list',
        props: {
            list: {
                // 列表
                type: Array,
                required: true
            },
            title: {
                // 标题
                type: String,
                default: ''
            },
            bottom: {
                //是否要下划线
                type: Boolean,
                default: true
            }
        },
    }
</script>

<style scoped lang="scss">
    .list {
        position: relative;
        border-radius: 2px;

        .title {
            padding: 20px 20px 10px 15px;
            font-size: 14px;
            font-weight: bold;
            color: #333;
            /*border-bottom: 1px solid hsla(0,0%,58.8%,.1)*/
        }

        .sidebar-list-item {
            padding: 0 20px;
            overflow: hidden;
            display: block;
            transition: .3s ease-in-out;
        }

        .need_bottom {
            border-bottom: 1px solid #e4e7ed;
        }

        .sidebar-list-item:hover {
            background-color: #f5f7fa;
            width: 100%;
            padding: 0 15px;
            font-weight: bold;
            /*	color: #b53c57;*/
        }
    }

</style>
