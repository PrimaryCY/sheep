<template>
  <div class="wrap">
    <div class="head">
      <el-row type="flex">
        <el-col>
        </el-col>
        <el-col :span="17">
          <el-input
            size="mini"
            type="text"
            placeholder="请输入关键字"
            clearable
            v-model="params.search"
            @keyup.enter.native="search"
          ></el-input>
        </el-col>
        <el-col :span="2">
          <div class="search-btn">
            <el-button
              plain
              @click="search"
              size="mini">
              搜索🔍
            </el-button>
          </div>
        </el-col>
      </el-row>
    </div>

    <el-divider>🔍</el-divider>
    <div class="content">
      <div class="left">
        <el-tabs
          @tab-click="change_post_type"
          v-model="params.post_type"
          tab-position="left"
          style="width: 100px;height: 100%">
          <el-tab-pane label="综合" name="0"></el-tab-pane>
          <el-tab-pane label="文章" name="1"></el-tab-pane>
          <el-tab-pane label="问答" name="2"></el-tab-pane>
        </el-tabs>
      </div>
      <div class="right">
        <list
          :need_border_top="false"
          :list="data.results">
          <template v-slot:item-content="data">
            <common_post_item
              :post="data.item">
            </common_post_item>
          </template>
        </list>
      </div>
      <div class="footer-pagination">
        <pagination
          ref="pagination"
          @change="_search"
          :pagination_config="{layout:'total, prev, pager, next',background:true}"
          :params="params"
          :pager="data"></pagination>
      </div>
    </div>
  </div>
</template>

<script>
  import list from '../../../components/list/list'
  import common_post_item from '../../../components/list/item/common_post_item'
  import pagination from '../../../components/pagination'
  import {api_s} from '../../../api'

  export default {
    name: 'search',
    data(){
      return {
        params:{
          search:'',
          post_type:'0'
        },
        data:{}
      }
    },
    async asyncData(context){
      let params,res
      params = {
        search:context.query.keyword,
        post_type: '0',
        offset:0,
        limit:15
      }
      try {
        let async_list = [
          api_s.list(params),
        ];
        [res] = await Promise.all(async_list)
      }catch(e)
      {
        context.error({statusCode:500,message:'ssr internal server error'})
      }
      return {
        params,
        data:res.data.data
      }
    },
    methods:{
      change_post_type(){
        this.$refs['pagination'].reset_params()
        this._search()
      },
      search(){
        this._search()
      },
      async _search(){
        this.move_to_top()
        // 获取用户个人帖子
        let loading = this.openLoading({
          target:'.right'
        })
        let res = await api_s.list(this.params)
        res = res.data
        if(res.code!==2000){
          this.$message(res.msg)
          loading.close()
          return
        }
        this.data=res.data
        loading.close()
      },
    },
    inject:['move_to_top'],
    components:{
      list,
      common_post_item,
      pagination
    }
  }
</script>

<style scoped lang="scss">
  .wrap{
    margin: 0 -39px;
    .head{
      margin-top: 10px;
      .search-btn{
        height: 100%;
        display: flex;
      }
    }
    .content{
      .left{
        position: absolute;
      }
      .right{
        margin-left: 85px;
        text-align: initial;
      }
    }
    .footer-pagination{
      padding: 25px;
      text-align: center;
    }
  }

</style>
