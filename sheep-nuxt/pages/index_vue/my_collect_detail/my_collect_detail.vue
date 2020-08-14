<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
	<div class="wrap">
		<div v-if="not_found" class="not-found-body">
			<div class="header">
				<el-page-header @back="push({name:'my_collect'})" title="返回">
					<div class="title-wrap" slot="content">
						<h1  class="title">
							未找到
						</h1>
<!--						<div class="byline desc">-->
<!--						</div>-->
					</div>
				</el-page-header>
			</div>
			<el-divider>❌</el-divider>
			<not_data text="没有该收藏集!"></not_data>
		</div>
		<div v-else class="detail-body">
			<div class="header">
				<el-page-header @back="push({name:'my_collect'})" title="返回">
					<div class="title-wrap" slot="content">
						<h1  class="title">
							{{collect_desc.name}}
						</h1>
						<div v-if="collect_desc.desc" class="byline desc">
							{{collect_desc.desc}}
						</div>
					</div>
				</el-page-header>
			</div>
			<el-divider>
				<img	v-show="collect_desc.image"
							:src="collect_desc.image"
							class="collect-image">
			</el-divider>
			<div id="l" class="content">
				<el-form  label-position="left" ref="filter_collect">
					<el-row type="flex" :gutter="20">
						<el-col :span="16">
							<el-form-item
											label-width="60px"
											label="关键字:">
								<el-input placeholder="文章名称"
													clearable
													size="small"
													maxlength="100"
													show-word-limit
													v-model="form.search"></el-input>
							</el-form-item>
						</el-col>
						<el-col :span="6">
							<el-form-item
											label-width="45px"
											label="类别:">
								<el-cascader
												ref="cascader"
												clearable
												size="small"
												:options="option.post_category"
												v-model="form.post_category"
												:props="{value:'id',label:'name',children:'child'}"
												:show-all-levels="false">
									<template slot-scope="{ node, data }">
										<span>{{ data.name }}</span>
										<span v-if="!node.isLeaf"> ({{ data.child.length }}) </span>
									</template>
								</el-cascader>
							</el-form-item>
						</el-col>
					</el-row>
					<el-row type="flex" :gutter="20">
						<el-col :span="12">
							<el-form-item
											label-width="75px"
											label="收藏日期:">
								<el-date-picker
												v-model="form.collect_time_range"
												type="daterange"
												align="right"
												unlink-panels
												range-separator="至"
												start-placeholder="开始日期"
												value-format="yyyy-MM-dd"
												end-placeholder="结束日期"
												size="small"
												:picker-options="pickerOptions">
								</el-date-picker>
							</el-form-item>
						</el-col>
						<el-col :span="7">
							<el-form-item
											label-width="75px"
											label="类型:">
								<el-radio-group v-model="form.post_type">
									<el-radio :label="1">文章</el-radio>
									<el-radio :label="2">提问</el-radio>
								</el-radio-group>
							</el-form-item>
						</el-col>
						<el-col :span="5">
							<el-form-item>
								<el-button type="primary" @click="filter_collect" size="small">查询</el-button>
								<el-button type="danger" @click="form={}" size="small">重置</el-button>
							</el-form-item>
						</el-col>
					</el-row>
				</el-form>
				<list
								:need_border_top="false"
								:list="collect_data.results">
					<template v-slot:item-content="data">
						<collect_post_item
										:post="data.item">
						</collect_post_item>
					</template>
				</list>
				<div class="collect-pagination">
					<pagination
									@change="_get_collect_data"
									:pagination_config="{layout:'total, sizes, prev, pager, next',background:true}"
									:params="params"
									:pager="collect_data"></pagination>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
    import {mapState} from 'vuex'

  import {
    api_user_collect_category,
		api_user_collect
  } from '../../../api'
	import not_data from '@/components/not_data'
    import list from '@/components/list/list'
    import collect_post_item from '@/components/list/item/collect_post_item'
	import {pickerOptions} from '../../../utils/util'
    import pagination from '../../../components/pagination'


  export default {
        name: 'my_collect_detail',
		data(){
            return {
          pickerOptions,
          not_found:false,
          collect_desc:{
					name:'读取中...',
					desc:'数据正在快马加鞭的赶过来!'
				},
          collect_data:{},
          params:{
          limit:10,
          offset:0,
          collect_id: this.$route.params.id,
				},
				form:{
          name:null,
          ordering:null,
          post_type:null,
				}
			}
		},
		methods:{
			async _get_collect_desc(){
				// 获取收藏集简介,标题之类的
				let id = this.$route.params.id
				let res = await api_user_collect_category.retrieve(id)
				res =res.data
				if(res.code === 404){
					return this.not_found = true
				}else if(res.code !== 2000){
					// loading.close()
          return this.$message(res.msg)
				}
				this.collect_desc = res.data
        this.not_found = false
			},
			async _get_collect_data(){
				// 获取收藏集内的文章/问答数据
				this.move_to_top()
                let loading = this.openLoading({
                text:'加载中...',
                target:'#l'
                })
                let res = await api_user_collect.list(this.params)
                res =res.data
                if(res.code !== 2000){
                    loading.close()
                    return this.$message(res.msg)
                }
                this.collect_data = res.data
                loading.close()
			},
			filter_collect(){
                // 点击查询
                if(this.form.collect_time_range){
                  this.params.start_collect_time=this.form.collect_time_range[0]
                  this.params.end_collect_time=this.form.collect_time_range[1]
                }else{
                  this.params.start_collect_time=null
                  this.params.end_collect_time=null
                }
                if(this.form.post_category){
                  this.params.category=this.form.post_category[this.form.post_category.length-1]
                }else {
                  this.params.category=null
                }
                this.params.search = this.form.search
                        this.params.post_type = this.form.post_type
                this._get_collect_data()
                    }
                },
		created () {
              if(process.server)return
                    this._get_collect_desc()
                    this._get_collect_data()
                },
        computed:{
          ...mapState(['option'])
        },
		inject:['push', 'move_to_top'],
		components:{
          not_data,
                list,
                collect_post_item,
                pagination
            }
  }
</script>

<style scoped lang="scss">
	/deep/ .el-page-header__title{
		align-self: center;
	}

	.wrap{
		.not-found-body{
			width: 100%;
		}
		.detail-body{
			width: 100%;
		}

		.header{
			margin-top: 5vh;
			margin-bottom: 5vh;
			.title-wrap{
				text-align: left;
				.title{
					font-weight: bold;
					font-size: 24px;
				}
				.desc{
					font-size: 10px;
				}
			}
		}
		.collect-image{
			width: 50px;
			height: 50px;
			border-radius: 5px;
			object-fit: cover;
			cursor: pointer;
		}
		.content{
			min-height: 40vh;
			.collect-pagination{
					padding: 8%;
					text-align: center;
			}
		}
	}
</style>
