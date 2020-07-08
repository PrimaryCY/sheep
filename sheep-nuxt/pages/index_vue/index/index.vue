<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
	<div>
    <div class="top">
      <div class="container">
        <input type="text" placeholder="Search...">
        <div class="search"></div>
      </div>
      <div class="menuList">
        <ul>
          <li :class="{active:params.category===0}">
            <a
              :href="$router.resolve({name:'index',query:{category:0}}).href">
              推荐
            </a>
          </li>
          <li v-for="(item,index) in option.post_category"
              :class="{active:item.id===params.category}"
              :key="item.id">
            <a
              :href="generate_url({name:'index',query:{category:item.id}})">
              {{item.name}}
            </a>
          </li>
        </ul>
      </div>
      <el-carousel
        v-if="banner.length"
        :interval="4000"
        type="card"
        height="263px"
        arrow="never">
        <el-carousel-item v-for="item in banner" :key="item.id" class="radius">
          <a
            target="_blank"
            :href="generate_url({name:'post_detail',params:{id:item.id}})"
            class="banner-wrap">
            <img :src="item.image" class="banner-image">
            <div class="banner-text">
              {{item.name}}
            </div>
          </a>
        </el-carousel-item>
      </el-carousel>
    </div>
    <div class="content">
      <div class="left">
        <div v-for="(post,index) in posts" :key="post.id">
          <el-row>
            <el-col>
              {{post}}
            </el-col>
          </el-row>
        </div>
      </div>
      <div class="right">
        <sidebar_item
          :list="hot"
          title="热门推荐">
          <template v-slot:item-content="data">
            <svg class="icon-min" aria-hidden="true">
              <use xlink:href="#icon-huo"></use>
            </svg>
            {{ data.item.name }}
          </template>
        </sidebar_item>

        <div class="newest">

        </div>
      </div>
    </div>
    <div>

    </div>

<!--							&lt;!&ndash; Post &ndash;&gt;-->
<!--							<article class="is-post is-post-excerpt">-->
<!--								<header>-->
<!--									<h2><a href="#">Welcome to Striped</a></h2>-->
<!--									<span class="byline">A free, fully responsive HTML5 site template by AJ for HTML5 Up!</span>-->
<!--								</header>-->
<!--								<div class="info">-->
<!--									<span class="date"><span class="month">Jan<span>uary</span></span> <span class="day">14</span><span class="year">, 2013</span></span>-->
<!--									<ul class="stats">-->
<!--										<li><a href="#" class="link-icon24 link-icon24-1">16</a></li>-->
<!--										<li><a href="#" class="link-icon24 link-icon24-2">32</a></li>-->
<!--										<li><a href="#" class="link-icon24 link-icon24-3">64</a></li>-->
<!--										<li><a href="#" class="link-icon24 link-icon24-4">128</a></li>-->
<!--									</ul>-->
<!--								</div>-->
<!--&lt;!&ndash;								<a href="#" class="image image-full"><img src="../../../static/img/n33-robot-invader.jpg" alt="" /></a>&ndash;&gt;-->
<!--								<p>-->
<!--									<strong>Hello!</strong> You're looking at <a href="#striped/">Striped</a>, a fully responsive HTML5 site template designed by AJ-->
<!--									for <a href="http://sc.chinaz.com/" title="站长素材">站长素材</a> It features a clean, minimalistic design, styling for all basic page elements (including blockquotes, tables and lists), a-->
<!--									repositionable sidebar (left or right), and HTML5/CSS3 code designed for quick and easy customization (see code comments for details).-->
<!--								</p>-->
<!--								<p>-->
<!--									Striped is released for free under the <a href="#">Creative Commons Attribution license</a> so feel free to use it for personal projects-->
<!--									or even commercial ones &ndash; just be sure to credit <a href="http://sc.chinaz.com/" title="站长素材">站长素材</a> for the design. If you like what you see here, be sure to check out-->
<!--									<a href="http://sc.chinaz.com/" title="站长素材">站长素材</a> for more cool designs or follow me on <a href="#">Twitter</a> for new releases and updates.-->
<!--								</p>-->
<!--							</article>-->

<!--							&lt;!&ndash; Post &ndash;&gt;-->
<!--							<article class="is-post is-post-excerpt">-->
<!--								<header>-->
<!--									<h2><a href="#">Lorem ipsum dolor sit amet</a></h2>-->
<!--									<span class="byline">Feugiat interdum sed commodo ipsum consequat dolor nullam metus</span>-->
<!--								</header>-->
<!--								<div class="info">-->
<!--									<span class="date"><span class="month">Jan<span>uary</span></span> <span class="day">8</span><span class="year">, 2013</span></span>-->
<!--									<ul class="stats">-->
<!--										<li><a href="#" class="link-icon24 link-icon24-1">12</a></li>-->
<!--										<li><a href="#" class="link-icon24 link-icon24-2">24</a></li>-->
<!--										<li><a href="#" class="link-icon24 link-icon24-3">48</a></li>-->
<!--										<li><a href="#" class="link-icon24 link-icon24-4">96</a></li>-->
<!--									</ul>-->
<!--								</div>-->
<!--&lt;!&ndash;								<a href="#" class="image image-full"><img src="../../../static/img/fotogrph-dark-stairwell.jpg" alt="" /></a>&ndash;&gt;-->
<!--								<p>-->
<!--									Quisque vel sapien sit amet tellus elementum ultricies. Nunc vel orci turpis. Donec id malesuada metus.-->
<!--									Nunc nulla velit, fermentum quis interdum quis, tate etiam commodo lorem ipsum dolor sit amet dolore.-->
<!--									Quisque vel sapien sit amet tellus elementum ultricies. Nunc vel orci turpis. Donec id malesuada metus.-->
<!--									Nunc nulla velit, fermentum quis interdum quis, convallis eu sapien. Integer sed ipsum ante.-->
<!--								</p>-->
<!--							</article>-->

							<!-- Pager -->
							<div class="pager">
								<!--<a href="#" class="button previous">Previous Page</a>-->
								<div class="pages">
									<a href="#" class="active">1</a>
									<a href="#">2</a>
									<a href="#">3</a>
									<a href="#">4</a>
									<span>&hellip;</span>
									<a href="#">20</a>
								</div>
								<a href="#" class="button next">Next Page</a>
							</div>

						</div>
</template>

<script>
  import {mapState} from 'vuex'

  import {
    api_banner,
    api_post,
    api_hot} from '../../../api'
  import sidebar_item from '../../../components/list/item/sidebar-item'


  export default {
    name: "index",
    data(){
      return {
        input:'',
        banner:[],
        hot:[],
        posts:[],
        tab_category:'0',
        params:{
          category:null,
        }
      }
    },
    async asyncData(context){
      console.log(context.query.category)
      let post_query = {
        category:context.query.category?Number(context.query.category):0
      }
      try {
        let banner, hot, posts
        let res = {
          'banner':[],
          'hot':[],
          'posts':[],
          'params':post_query
        }
        let async_list = [
          api_hot.list(),
          api_post.list(post_query)
        ]
        if(post_query.category===0){
          async_list.unshift(api_banner.list());
          [banner, hot, posts] = await Promise.all(async_list)
          res.banner = banner.data.data
        }else {
          [hot, posts] = await Promise.all(async_list)
        }
        res.hot = hot.data.data
        res.posts = posts.data.data.results
        return res
      }catch(e)
      {
        context.error({statusCode:500,message:'ssr internal server error'})
      }
    },
    inject:['generate_url'],
    methods: {
    },
    computed:{
      ...mapState(['option'])
    },
    components:{
      sidebar_item
    }
  }
</script>

<style scoped lang="scss">
  .banner-wrap{
      position: relative;
      height: 100%;
      display: block;
      .banner-image{
        width: 100%;
        height: 100%;
        border-radius: 25px;
        object-fit: cover;
      }
      .banner-text{
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 30px 0 12px 15px;
        font-family: PingFangSC-Medium;
        font-weight: 500;
        font-size: 18px;
        color: #fff;
        width: 100%;
        text-align: left;
        background: url('/img/banner_layer.png') no-repeat
      }
    }
  .el-carousel__item--card.is-in-stage{
    max-width: 580px;
    min-width: 35vw;
  }


  .top{
    width: 100%;
    .menuList {
      /*width: 800px;*/
      /*height: 60px;*/
      padding-bottom: 10px;
      .active {
        border-bottom: 2px solid #364045;
        a{
          color: black;
        }
      }
      ul {
        /*width: 100%;*/
        height: 100%;
        display: flex;
        list-style: none;
        padding: 0;
        margin: 0;
        font-size: 16px;
        line-height: 45px;
        border-bottom: 1px solid #e4e7ed;
        li {
          /*flex: 0 0 100px;*/
          margin: 0 20px;
          text-align: center;
          cursor: pointer;
          a{
            display: block;
            height: 100%;
            color: #717181;
          }
        }
      }
    }

    .container {
      position:relative;
      /*margin: auto;*/
      margin-bottom: 30px;
      /*top: 0;*/
      /*left: 0;*/
      right: 0;
      /*bottom: 0;*/
      width: 34vw;
      height: 80px;
    }
    .container .search {
      position: absolute;
      margin: auto;
      top: 0;
      right: -100%;
      bottom: 0;
      /*left: 0;*/
      width: 45px;
      height: 45px;
      background: crimson;
      border-radius: 50%;
      transition: all 1s;
      z-index: 4;
      box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.4);
    }
    .container .search:hover {
      cursor: pointer;
    }
    .container .search::before {
      content: "";
      position: absolute;
      margin: auto;
      top: 17px;
      right: 0;
      bottom: 0;
      left: 17px;
      width: 12px;
      height: 2px;
      background: white;
      transform: rotate(45deg);
      transition: all .5s;
    }
    .container .search::after {
      content: "";
      position: absolute;
      margin: auto;
      top: -5px;
      right: 0;
      bottom: 0;
      left: -5px;
      width: 15px;
      height: 15px;
      border-radius: 50%;
      border: 2px solid white;
      transition: all .5s;
    }
    .container input {
      font-family: 'Inconsolata', monospace;
      position: absolute;
      margin: auto;
      top: 0;
      right: -100%;
      bottom: 0;
      /*left: 0;*/
      width: 40px;
      height: 40px;
      outline: none;
      border: none;
      background: crimson;
      color: white;
      text-shadow: 0 0 10px crimson;
      padding: 0 80px 0 20px;
      border-radius: 30px;
      box-shadow: 0 0 5px 0 crimson, 0 20px 25px 0 rgba(0, 0, 0, 0.2);
      transition: all 1s;
      opacity: 0;
      z-index: 5;
      font-weight: 500;
      letter-spacing: 0.1em;
    }
    .container input:hover {
      cursor: pointer;
    }
    .container input:focus {
      width: 600px;
      opacity: 1;
      cursor: text;
    }
    .container input:focus ~ .search {
      background: #151515;
      z-index: 6;
    }
    .container input:focus ~ .search::before {
      top: 0;
      left: 0;
      width: 25px;
    }
    .container input:focus ~ .search::after {
      top: 0;
      left: 0;
      width: 25px;
      height: 2px;
      border: none;
      background: white;
      border-radius: 0%;
      transform: rotate(-45deg);
    }
    .container input::placeholder {
      color: white;
      opacity: 0.5;
      font-weight: bolder;
    }
  }

  .content{
    text-align: initial;
    font-size: 0;
    .left{
      font-size: 14px;
      width: 80%;
      display: inline-block;
      /*background: gold;*/
      vertical-align: top;
    }
    .right{
      width: 20%;
      font-size: 14px;
      display: inline-block;
      padding-left: 10px;
      .hot{
        .hot-title{
          display: -webkit-box;
          display: -ms-flexbox;
          display: flex;
          -webkit-box-align: center;
          -ms-flex-align: center;
          align-items: center;
          font-size: 16px;
          color: #4a4a4a;
          height: 24px;
          line-height: 24px;
          margin-bottom: 5px;
          position: relative;
          .line{
            display: block;
            float: left;
            width: 3px;
            height: 16px;
            background: #cf2730;
            overflow: hidden;
            margin-right: 5px;
          }
          .txt{
            display: block;
            float: left;
            font-size: 16px;
            color: #2c3033;
          }
        }
        .sidebar-list-item {
          margin-bottom: 10px;
          height: 48px;
          display: block;
          border-bottom: 1px solid #e4e7ed;
          .img-box {
            float: left;
            margin-right: 10px;
            position: relative;

            img {
              cursor: pointer;
              position: relative;
              /*display: inline-block;*/
              display: block;
              width: 64px;
              height: 48px;
              border-radius: 3px;
              vertical-align: top;
              -o-object-fit: cover;
              object-fit: cover;
            }
          }

          .content {
            padding-top: 2px;
            .company_name{
              display: block;
              margin-bottom: 3px;
              font-size: 12px;
              color: #3d3d3d;
              letter-spacing: 0;
              line-height: 22px;
              max-width: 200px;
              overflow: hidden;
              cursor: pointer;
              font-weight: bold;
              text-overflow: -o-ellipsis-lastline;
              text-overflow: ellipsis;
              display: -webkit-box;
              -webkit-line-clamp: 2;
              line-clamp: 2;
              -webkit-box-orient: vertical;
            }
          }
        }
      }
    }

  }
</style>
