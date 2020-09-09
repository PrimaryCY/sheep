<template>
    <!-- Right -->
    <div>
        <div v-if="position==='right'" class="receiver">
            <div>
                <slot name="user"></slot>
                <!--      <img src="chatTemplateExample2_files/cat.jpg">-->
            </div>
            <div style="max-width: 80%" class="receiver_content">
                <div class="right_triangle"></div>
                <span> {{text}} </span>
                <p v-if="time" class="bottom">
                    {{time}}
                </p>
            </div>
            <div style="clear: both"></div>
        </div>
        <!-- Left -->
        <div v-else>
            <div class="sender">
                <div>
                    <slot name="user"></slot>
                </div>
                <div style="max-width: 80%">
                    <div class="left_triangle"></div>
                    <span> {{text}} </span>
                </div>
            </div>
            <div style="clear: both"></div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'bubble_text',
        props: {
            text: {
                type: String,
                required: true
            },
            position: {
                type: String,
                default() {
                    return 'right'
                }
            },
            time: {
                type: String,
                required: false
            }
        }
    }
</script>

<style scoped lang="scss">
    /* bubble style */
    .sender {
        clear: both;
    }

    .sender div:nth-of-type(1) {
        float: left;
    }

    .sender div:nth-of-type(2) {
        background-color: aquamarine;
        float: left;
        margin: 0 20px 10px 15px;
        padding: 10px 10px 10px 0px;
        border-radius: 7px;
    }

    /*.receiver div:first-child img,*/
    /*.sender div:first-child img{*/
    /*  width:45px;*/
    /*  height: 45px;*/
    /*}*/
    img {
        width: 45px;
        height: 45px;
    }

    .receiver {
        clear: both;
        margin-bottom: 5px;
    }

    .receiver div:nth-child(1) {
        float: right;
    }

    .receiver div:nth-of-type(2) {
        float: right;
        background-color: #f7f4e5;
        margin: 0 10px 0px 20px;
        padding: 10px 0px 10px 10px;
        border-radius: 7px;
    }

    .left_triangle {
        height: 0px;
        width: 0px;
        border-width: 8px;
        border-style: solid;
        border-color: transparent aquamarine transparent transparent;
        position: relative;
        left: -16px;
        top: 3px;
    }

    .right_triangle {
        height: 0px;
        width: 0px;
        border-width: 8px;
        border-style: solid;
        border-color: transparent transparent transparent #f7f4e5;
        position: relative;
        right: -16px;
        top: 3px;
    }

    .bottom {
        position: absolute;
        font-size: 10px;
        font-weight: 400;
        margin: 5px 0;
        text-align: right;
    }
</style>
