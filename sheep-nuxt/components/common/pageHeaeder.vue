<template>
    <div class="header">
        <div class="page-header">
            <div class="page-header__left">
                <div class="page-header__title">
                </div>
            </div>
            <div class="page-header__content">
                <div class="title-wrap">
                    <h1 class="title">
                        {{text}}
                    </h1>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "pageHeaeder",
        props: {
            text: {
                type: String,
                required: true
            },
        }
    }
</script>

<style scoped lang="scss">
    .header {
        margin-top: 5vh;
        margin-bottom: 5vh;

        .page-header {
            display: flex;
            line-height: 24px;

            .page-header__left {
                display: flex;
                cursor: pointer;
                margin-right: 40px;
                position: relative;

                .page-header__title {
                    align-self: center;
                    font-size: 14px;
                    font-weight: 500;
                }
            }
        .page-header__left:after {
            content: "";
            position: absolute;
            width: 1px;
            height: 16px;
            right: -20px;
            top: 50%;
            transform: translateY(-50%);
            background-color: #dcdfe6;
        }

            .page-header__content {
                font-size: 18px;
                color: #303133;

                .title-wrap {
                    text-align: left;

                    .title {
                        font-weight: bold;
                        font-size: 24px;
                    }
                }
            }
        }
    }

</style>