<template>
	<div>
    <div class="top">
      <el-carousel :interval="4000" type="card" height="200px" arrow="never">
        <el-carousel-item v-for="item in 6" :key="item">
          <h3 class="medium">{{ item }}</h3>
        </el-carousel-item>
      </el-carousel>
      <div class="container">
        <input type="text" placeholder="Search...">
        <div class="search"></div>
      </div>
    </div>
    <div class="content">
      <div class="first">

      </div>
      <div class="second">

      </div>
    </div>

							<!-- Post -->
							<article class="is-post is-post-excerpt">
								<header>
									<h2><a href="#">Welcome to Striped</a></h2>
									<span class="byline">A free, fully responsive HTML5 site template by AJ for HTML5 Up!</span>
								</header>
								<div class="info">
									<span class="date"><span class="month">Jan<span>uary</span></span> <span class="day">14</span><span class="year">, 2013</span></span>
									<ul class="stats">
										<li><a href="#" class="link-icon24 link-icon24-1">16</a></li>
										<li><a href="#" class="link-icon24 link-icon24-2">32</a></li>
										<li><a href="#" class="link-icon24 link-icon24-3">64</a></li>
										<li><a href="#" class="link-icon24 link-icon24-4">128</a></li>
									</ul>
								</div>
<!--								<a href="#" class="image image-full"><img src="../../../static/img/n33-robot-invader.jpg" alt="" /></a>-->
								<p>
									<strong>Hello!</strong> You're looking at <a href="#striped/">Striped</a>, a fully responsive HTML5 site template designed by AJ
									for <a href="http://sc.chinaz.com/" title="站长素材">站长素材</a> It features a clean, minimalistic design, styling for all basic page elements (including blockquotes, tables and lists), a
									repositionable sidebar (left or right), and HTML5/CSS3 code designed for quick and easy customization (see code comments for details).
								</p>
								<p>
									Striped is released for free under the <a href="#">Creative Commons Attribution license</a> so feel free to use it for personal projects
									or even commercial ones &ndash; just be sure to credit <a href="http://sc.chinaz.com/" title="站长素材">站长素材</a> for the design. If you like what you see here, be sure to check out
									<a href="http://sc.chinaz.com/" title="站长素材">站长素材</a> for more cool designs or follow me on <a href="#">Twitter</a> for new releases and updates.
								</p>
							</article>

							<!-- Post -->
							<article class="is-post is-post-excerpt">
								<header>
									<h2><a href="#">Lorem ipsum dolor sit amet</a></h2>
									<span class="byline">Feugiat interdum sed commodo ipsum consequat dolor nullam metus</span>
								</header>
								<div class="info">
									<span class="date"><span class="month">Jan<span>uary</span></span> <span class="day">8</span><span class="year">, 2013</span></span>
									<ul class="stats">
										<li><a href="#" class="link-icon24 link-icon24-1">12</a></li>
										<li><a href="#" class="link-icon24 link-icon24-2">24</a></li>
										<li><a href="#" class="link-icon24 link-icon24-3">48</a></li>
										<li><a href="#" class="link-icon24 link-icon24-4">96</a></li>
									</ul>
								</div>
<!--								<a href="#" class="image image-full"><img src="../../../static/img/fotogrph-dark-stairwell.jpg" alt="" /></a>-->
								<p>
									Quisque vel sapien sit amet tellus elementum ultricies. Nunc vel orci turpis. Donec id malesuada metus.
									Nunc nulla velit, fermentum quis interdum quis, tate etiam commodo lorem ipsum dolor sit amet dolore.
									Quisque vel sapien sit amet tellus elementum ultricies. Nunc vel orci turpis. Donec id malesuada metus.
									Nunc nulla velit, fermentum quis interdum quis, convallis eu sapien. Integer sed ipsum ante.
								</p>
							</article>

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

  export default {
    name: "index",
    data(){
      return {
        input:''
      }
    },
    methods: {
    },
  }
</script>

<style scoped lang="scss">
  .S{width:160px;height:50px;position: relative;}
  .S:before{content: ''; display: block;border:10px solid transparent;border-top-color:red;border-right-color:red; width:50px;height: 50px; border-radius:40px;background:transparent;transform:rotateZ(-45deg);position: absolute;}
  .S:after{content: ''; display: block;border:10px solid transparent;border-bottom-color:red;border-right-color:red; width:50px;height: 50px; border-radius:40px;background:transparent;transform:rotateZ(45deg);position: absolute;top:-5px;left:60px}


  .top{
    .container {
      position:relative;
      margin: auto;
      margin-bottom: 30px;
      top: 0;
      /*left: 0;*/
      right: 0;
      bottom: 0;
      width: 300px;
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
    .first{
      border-top: 2px solid black;
      border-left: 2px solid black;
      width: 100%;
      height: 400px;
      border-radius: 20%;
    }
    .second{
      border-right: 2px solid black;
      border-bottom: 2px solid black;
      width: 100%;
      height: 400px;
      border-top-left-radius: 0!important;
      border-radius: 20%;
    }
  }
</style>
