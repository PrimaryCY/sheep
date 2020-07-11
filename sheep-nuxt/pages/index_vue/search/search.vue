<template>
  <div>
    search:{{keyword}}
  </div>
</template>

<script>
  export default {
    name: 'search',
    data(){
      return {
        keyword:''
      }
    },
    asyncData(context){
      return {
        keyword: context.query.keyword,
      }
    }
  }
</script>

<style scoped>

</style>
