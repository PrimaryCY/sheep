<template>
	<div>
    <div class="top">
      <div class="container">
        <input type="text" placeholder="Search...">
        <div class="search"></div>
      </div>
      <el-tabs v-model="params.category" @tab-click="change_category">
        <el-tab-pane  label="推荐">
        </el-tab-pane>
        <el-tab-pane v-for="category in option.post_category"
                     :key="category.id"
                     :name="`${category.id}`"
                     :label="category.name">
        </el-tab-pane>
      </el-tabs>
      <el-carousel :interval="4000" type="card" height="263px" arrow="never">
        <el-carousel-item v-for="item in banner" :key="item.id" class="radius">
          <div class="banner-wrap">
            <img :src="item.image" class="banner-image">
            <div class="banner-text">
              {{item.name}}
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>
    <div class="content">
      <div class="left">
        {{post}}
      </div>
      <div class="right">
        <ul>
          <li v-for="i in hot" :key="i.id">
            {{i.name}}
          </li>
        </ul>
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
  import {
    api_banner,
    api_post,
    api_hot} from '../../../api'
  import {mapState} from 'vuex'


  export default {
    name: "index",
    data(){
      return {
        input:'',
        banner:[],
        hot:[],
        post:[],
        tab_category:'0',
        params:{
          category:null,
        }
      }
    },
    async asyncData(context){
      let post_params = {
        category:context.params.id===0?null:context.params.id
      }
      try {
        let [banner, hot, post] = await Promise.all([
          api_banner.list(),
          api_hot.list(),
          api_post.list(post_params)
        ])
        banner = banner.data.data
        hot = hot.data.data
        post = post.data.data
        return {
          banner,
          hot,
          post,
          params:post_params
        }
      }catch(e)
      {
        context.error({statusCode:500,message:'ssr internal server error'})
      }
    },
    methods: {
      change_category(){
        let params = {
          id:this.tab_category
        }
        this.$router.push({
          'name':'index-detail',
          params
        })
      }
    },
    computed:{
      ...mapState(['option'])
    }
  }
</script>

<style scoped lang="scss">
  .banner-wrap{
      position: relative;
      height: 100%;
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
      background: gold;
      vertical-align: top;
    }
    .right{
      width: 20%;
      font-size: 14px;
      display: inline-block;
      background: #00feff;
    }

  }
</style>
