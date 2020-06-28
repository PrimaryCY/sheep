<template>
  <div class="list">
    <!--增加tabindex属性  使focus对div起作用-->
    <transition-group tag="div">
      <div class="item" tabindex="0" v-for="item in list" :key="item.id">
        <slot name="item-content" :item="item">

        </slot>
      </div>
    </transition-group>
    <not_data :text="no_data_text"
              :list="list"></not_data>
  </div>
</template>

<script>
  import not_data from './not_data'

  export default {
    name: 'item',
    props:{
      list:{
        // type:Array,
        required:true
      },
      no_data_text:{
        type:String,
        default:'空空如也😭'
      }
    },
    components:{
      not_data
    }
  }
</script>

<style scoped lang="scss">
  .v-enter,.v-leave-to{
    opacity: 0;
    transform: translateX(-60px);
  }
  .v-enter-active,
  .v-leave-active{
    transition: all 0.6s ease;
  }

  .list{
    min-height: 80vh;
  .item{
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-direction: normal;
    -webkit-box-orient: vertical;
    -ms-flex-direction: column;
    flex-direction: column;
    border-top: 1px dotted #ddd;
    border-bottom: 1px dotted #ddd;
    padding: 1rem 1rem 1rem 1rem;
    color: #999;
    font-size: 14px;
  }

  .item:hover{
    background-color: #f5f7fa;
  }
  .item:focus{
    background-color: #ecf5ff;
    outline: 0;
    /*outline: -webkit-focus-ring-color auto 1px;*/
  }
  }
</style>
