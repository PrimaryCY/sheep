<template>
	<div id="app" class="mobileUI-main-content">
		<!-- Wrapper -->
		<div id="wrapper" :class="{'pack-up':this.pack_up}">

			<!-- Content -->
			<div id="content" class="mobile-main-content">
				<router-view id="content-inner"></router-view>
			</div>

			<div class="sidebar">
				<!--pack-up-button-->
				<div class="pack-up-btn">
					<el-switch
									v-model="pack_up"
									active-color="#7d7d83"
									inactive-color="#b53c57">
					</el-switch>
				</div>


				<div v-if="!user.username">
						<!-- Logo -->
						<div id="logo">
							<el-button
											type="danger"
											:loading="loginBtn.loading"
											class="login-btn"
											@click.prevent="login"
							>{{ loginBtn.loading ? '登陆中...' : '登录' }}</el-button>
						</div>
						<!-- Search -->
						<section class="is-search is-first">
							<form method="post" action="#">
								<input type="text" class="text" name="search" placeholder="Search" />
							</form>
						</section>
						<!-- Nav -->
						<nav id="nav" class="mobileUI-site-nav">
							<ul>
								<li><a href="#">所有帖子</a></li>
								<li><a href="#">意见反馈</a></li>
							</ul>
						</nav>
					</div>
				<div v-else>
						<!-- logo -->
						<div class="user" @click="push('/info',2)">
							<el-avatar :size="60" :src="user.portrait" >
								<img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"/>
							</el-avatar>
							<p class="username">
								<svg v-if="user.gender===0" class="icon-min" aria-hidden="true">
									<use xlink:href="#icon-xingbienv"></use>
								</svg>
								<svg v-else class="icon-min" aria-hidden="true">
									<use xlink:href="#icon-xingbienan"></use>
								</svg>
								&nbsp;
								<b>{{user.username}}</b>
							</p>
						</div>

						<!-- Search -->
						<section class="is-search is-first">
							<form method="post" action="#">
								<input type="text" class="text" name="search" placeholder="Search" />
							</form>
						</section>
						<!--postings-->
						<section class="is-search postings">
							<div id="postings">
								<el-button
												type="danger"
												class="login-btn"
												@click.prevent="blank_push('postings')"
								><svg class="icon-min" aria-hidden="true">
									<use xlink:href="#icon-fabu"></use>
								</svg>
									发表文章
								</el-button>
							</div>
						</section>

						<!--Nav-->
						<nav id="nav" class="mobileUI-site-nav">
							<ul>
								<li :class="{current_page_item:active==='/index'}" @click.prevent="push('/index')"><a href="#">
									<svg class="icon-min" aria-hidden="true">
										<use xlink:href="#icon-shiyongwendang"></use>
									</svg>
									所有文章
								</a></li>
								<li :class="{current_page_item:active==='/info'}" @click.prevent="push('/info')"><a href="#">
									<svg class="icon-min" aria-hidden="true">
										<use xlink:href="#icon-icon_zhanghao"></use>
									</svg>
									个人中心
								</a></li>
								<li :class="{current_page_item:active==='/my_post'}" @click.prevent="push('/my_post')"><a href="#">
									<svg class="icon-min" aria-hidden="true">
										<use xlink:href="#icon-chuangzuo"></use>
									</svg>
									我的文章
								</a></li>
								<li><a href="#">
									<svg class="icon-min" aria-hidden="true">
										<use xlink:href="#icon-shoucang"></use>
									</svg>
									我的收藏
								</a></li>
								<li><a href="#">
									<svg class="icon-min" aria-hidden="true">
										<use xlink:href="#icon-icon_community_line"></use>
									</svg>
									我的评论
								</a></li>
								<li><a href="#">
									<svg class="icon-min" aria-hidden="true">
										<use xlink:href="#icon-bofangjilu"></use>
									</svg>
									我的浏览
								</a></li>
								<li><a href="#">
									<svg class="icon-min" aria-hidden="true">
										<use xlink:href="#icon-yijianfankui"></use>
									</svg>
									意见反馈
								</a></li>
							</ul>
						</nav>
						<!--quit-->
						<section class="is-text-style1">
							<div class="inner" @click="quit()">
								<p>
									<svg class="icon-min" aria-hidden="true">
										<use xlink:href="#icon-switch"></use>
									</svg>
									<span>退出</span>
								</p>
							</div>
						</section>

					</div>

				<div>
<!--					<div v-if="!user.username">-->
<!--						&lt;!&ndash; Logo &ndash;&gt;-->
<!--						<div id="logo">-->
<!--							<el-button-->
<!--											type="danger"-->
<!--											:loading="loginBtn.loading"-->
<!--											class="login-btn"-->
<!--											@click.prevent="login"-->
<!--							>{{ loginBtn.loading ? '登陆中...' : '登录' }}</el-button>-->
<!--						</div>-->
<!--						&lt;!&ndash; Nav &ndash;&gt;-->
<!--						<nav id="nav" class="mobileUI-site-nav">-->
<!--							<ul>-->
<!--								<li><a href="#">所</a></li>-->
<!--								<li><a href="#">意</a></li>-->
<!--							</ul>-->
<!--						</nav>-->
<!--					</div>-->
<!--					<div v-else>-->
<!--						&lt;!&ndash; logo &ndash;&gt;-->
<!--						<div class="user" @click="push('/info',2)">-->
<!--							<el-avatar :size="50" :src="user.portrait" >-->
<!--								<img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"/>-->
<!--							</el-avatar>-->
<!--						</div>-->

<!--						&lt;!&ndash;postings&ndash;&gt;-->
<!--						<section class="is-search is-first">-->
<!--							<div id="postings">-->
<!--								<el-button-->
<!--												type="danger"-->
<!--												class="login-btn"-->
<!--												@click.prevent="blank_push('postings')"-->
<!--								>发</el-button>-->
<!--							</div>-->
<!--						</section>-->

<!--						&lt;!&ndash;Nav&ndash;&gt;-->
<!--						<nav id="nav" class="mobileUI-site-nav">-->
<!--							<ul>-->
<!--								<li :class="{current_page_item:active==='/index'}" @click.prevent="push('/index')"><a href="#">所</a></li>-->
<!--								<li :class="{current_page_item:active==='/info'}" @click.prevent="push('/info')"><a href="#">个</a></li>-->
<!--								<li :class="{current_page_item:active==='/my_post'}" @click="push('/my_post')"><a href="#">我</a></li>-->
<!--								<li><a href="#">我</a></li>-->
<!--								<li><a href="#">我</a></li>-->
<!--								<li><a href="#">我</a></li>-->
<!--								<li><a href="#">意</a></li>-->
<!--							</ul>-->
<!--						</nav>-->
<!--						&lt;!&ndash;quit&ndash;&gt;-->
<!--						<section class="is-text-style1">-->
<!--							<div class="inner" @click="quit()">-->
<!--								<p>-->
<!--									退出-->
<!--								</p>-->
<!--							</div>-->
<!--						</section>-->

<!--					</div>-->

				</div>
				<!-- Recent Posts -->
				<section class="is-recent-posts">
					<header>
						<h2>Recent Posts</h2>
					</header>
					<ul>
						<li><a href="#">Nothing happened</a></li>
						<li><a href="#">My Dearest Cthulhu</a></li>
						<li><a href="#">The Meme Meme</a></li>
						<li><a href="#">Now Full Cyborg</a></li>
						<li><a href="#">Temporal Flux</a></li>
					</ul>
				</section>

				<!-- Recent Comments -->
				<section class="is-recent-comments">
					<header>
						<h2>关于本站</h2>
					</header>
					<ul>
						<!--						<li><a href="#">关于本站</a></li>-->
						<li><a href="#">技术支持</a></li>
						<li><a href="#">github 地址</a></li>
					</ul>
				</section>

				<!-- Calendar -->
				<section class="is-calendar">

					<!--					<div class="inner">-->
					<!--						<table>-->
					<!--							<caption>February 2013</caption>-->
					<!--							<thead>-->
					<!--							<tr>-->
					<!--								<th scope="col" title="Monday">M</th>-->
					<!--								<th scope="col" title="Tuesday">T</th>-->
					<!--								<th scope="col" title="Wednesday">W</th>-->
					<!--								<th scope="col" title="Thursday">T</th>-->
					<!--								<th scope="col" title="Friday">F</th>-->
					<!--								<th scope="col" title="Saturday">S</th>-->
					<!--								<th scope="col" title="Sunday">S</th>-->
					<!--							</tr>-->
					<!--							</thead>-->
					<!--							<tbody>-->
					<!--							<tr>-->
					<!--								<td colspan="4" class="pad"><span>&nbsp;</span></td>-->
					<!--								<td><span>1</span></td>-->
					<!--								<td><span>2</span></td>-->
					<!--								<td><span>3</span></td>-->
					<!--							</tr>-->
					<!--							<tr>-->
					<!--								<td><span>4</span></td>-->
					<!--								<td><span>5</span></td>-->
					<!--								<td><a href="#">6</a></td>-->
					<!--								<td><span>7</span></td>-->
					<!--								<td><span>8</span></td>-->
					<!--								<td><span>9</span></td>-->
					<!--								<td><a href="#">10</a></td>-->
					<!--							</tr>-->
					<!--							<tr>-->
					<!--								<td><span>11</span></td>-->
					<!--								<td><span>12</span></td>-->
					<!--								<td><span>13</span></td>-->
					<!--								<td class="today"><a href="#">14</a></td>-->
					<!--								<td><span>15</span></td>-->
					<!--								<td><span>16</span></td>-->
					<!--								<td><span>17</span></td>-->
					<!--							</tr>-->
					<!--							<tr>-->
					<!--								<td><span>18</span></td>-->
					<!--								<td><span>19</span></td>-->
					<!--								<td><span>20</span></td>-->
					<!--								<td><span>21</span></td>-->
					<!--								<td><span>22</span></td>-->
					<!--								<td><a href="#">23</a></td>-->
					<!--								<td><span>24</span></td>-->
					<!--							</tr>-->
					<!--							<tr>-->
					<!--								<td><a href="#">25</a></td>-->
					<!--								<td><span>26</span></td>-->
					<!--								<td><span>27</span></td>-->
					<!--								<td><span>28</span></td>-->
					<!--								<td class="pad" colspan="3"><span>&nbsp;</span></td>-->
					<!--							</tr>-->
					<!--							</tbody>-->
					<!--						</table>-->
					<!--					</div>-->
				</section>

				<!-- Copyright -->
				<div id="copyright">
					<p>
						&copy; 2020 A personal Site.
					</p>
				</div>

			</div>

		</div>

	</div>
</template>

<script>
	import {mapState} from 'vuex'

	import {sleep} from '../../utils/util'

  export default {
    name: "index",
		inject:['push','blank_push'],
		data(){
      return {
				pack_up:false, // 是否展开收起
        loginBtn:{
          loading:false,
				},
			}
		},
		computed:{
			...mapState(['user']),
			active(){
				return this.$route.path
			}
		},
		methods:{
      async login(){
				console.log('login')
				this.loginBtn.loading = true
				await sleep(0.5)
				this.$router.push('/login')
				this.loginBtn.loading = false
			},
			async quit(){
				// 退出登录
				let res = await this.$confirm('此操作将退出登录?', '退出登录', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning',
					roundButton:true,
					customClass:'message'
				}).catch(()=>{
				})
				if (res==='confirm'){
					this.$store.dispatch('clear_userinfo')
				}
			}
		},
  }
</script>

<style scoped lang="scss">


	@media (min-width: 1200px) {
		.pack-up {
			.sidebar{
				width: 80px;
				padding: 1.5em 1em 1em 1em;
				/*登录按钮*/
				#logo{
					margin: 0;
					button{
						white-space: pre;
						letter-spacing: 18px;
						overflow: hidden;
						padding: 25%;
					}
				}
				/*发表文章按钮*/
				#postings{
					margin: 0;
					button{
						white-space: pre;
						letter-spacing: 18px;
						overflow: hidden;
						padding: 30%;
					}

				}
				/*用户信息*/
				.user{
					span{
						height: 50px!important;
						width: 50px!important;
					}
					.username{
						display: none;
					}
				}
				/*搜索框*/
				section:nth-child(2){
					display: none;
				}
				/*功能列表*/
				section,nav{
					overflow: hidden;
					li a{
						height: 39px;
						overflow: hidden;
					}
				}
				/*退出按钮*/
				.is-text-style1 .inner{
						overflow: hidden;
						p{
							height: 34px;
							overflow: hidden;
							svg{
								margin: 10px
							}
						}
					}
			}
			#content{
				margin-left: 12%!important;
				min-height: 118em;
				#content-inner{
					max-width: 95%;
				}
			}
		}
	}

	.pack-up-btn{
		margin-bottom: 15px;
		text-align: right;
	}
	.user{
		.username{
			padding-top: 2%;
			word-break: break-all;
			b{
				color: white;
			}
		}
	}
	#content{
		min-height: 106em;
		transition: margin-left 0.25s ease-in-out;
	}

	.sidebar {
		transition: width 0.25s ease-in-out;
		-moz-box-shadow:7px 0px 15px #595654;
		-webkit-box-shadow:7px 0px 15px #595654;
		box-shadow:7px 0px 15px #595654;
		border-top-right-radius:1%;
		border-bottom-right-radius:1%;
	}


	#logo{
		padding: 0;
		margin: 10px;
		.login-btn{
			background-color: #c94663;
			width: 100%;
			height: 85px;
			border: 0;
			font-size: 26px;
			margin: 0px;
		}
		.login-btn:active{
			background-color: #a14663;
		}
	}
	#postings{
		padding: 0;
		margin: 10px;
		.login-btn{
			background-color: #b53c57;
			width: 100%;
			height: 50px;
			border: 0;
			font-size: 20px;
			margin: 0;
		}
		.login-btn:active{
			background-color: #a14663;
		}
	}

</style>
