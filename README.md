# <font color=#ca0c16> Sheep 博客提问系统

**django+nuxt-vue+channels 实时在线聊天博客提问系统**
<br>
&nbsp;&nbsp;&nbsp;&nbsp;这是新开的一个开源项目,欢迎有兴趣加入的人可以通过下面我的联系方式联系本人,sheep 项目主要功能是发表博客,实时在线聊天,对感兴趣的博客进行收藏点赞,对喜欢的人进行关注.
<br>
&nbsp;&nbsp;&nbsp;&nbsp;特点是如果一篇博客踩的数量太多,系统会自动删除,保证了博客都是及时有效的,让无用文章消失在大众眼前
<br>
&nbsp;&nbsp;&nbsp;&nbsp;搜索系统本想有 elasticSearch 来做,可是远端云服务器费用昂贵,之后有条件,全局搜索可以上 elasticSearch 来做
</font>

---

### <font color=#ca0c16>项目进度</font>

**_已完成:_**

- 全站改为ssr
- 登录注册
- 发表文章(支持富文本+markdown)
- 个人资料修改
- 七牛云存储上传文件/图片
- 编辑文章
- 删除文章
- 我的文章
- 我的提问
- 提交反馈
- 历史反馈

**_未完成:_**

- 文章详情
- 我的收藏
- 点赞系统
- 好友关注系统
- 个人空间
- 在线实时聊天
- 搜索系统

---

### <font color=#ca0c16>项目建议/加入</font>

有什么更好的建议或者发现什么 bug,遇到部署问题可以联系我
<br>
同时欢迎对项目有兴趣的程序猿共同创造,最好要会 vue 或者 django.
<br>
项目详细需求文档在同目录下的prd.md中
<br>
个人 qq:907031027

---

### <font color=#ca0c16>项目展示</font>

<p align="center" >
<img name='register' src="https://img-blog.csdnimg.cn/20200427115631329.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQ4NTUwMg==,size_16,color_FFFFFF,t_70"/>

<img  name='index' src="https://img-blog.csdnimg.cn/20200427115631838.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQ4NTUwMg==,size_16,color_FFFFFF,t_70"/>

<img name='postings' src="https://img-blog.csdnimg.cn/20200427115631226.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQ4NTUwMg==,size_16,color_FFFFFF,t_70"/>

<img name='info' src="https://img-blog.csdnimg.cn/2020042711563193.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQ4NTUwMg==,size_16,color_FFFFFF,t_70"/>

<img name='feedback' src='https://img-blog.csdnimg.cn/20200612114143556.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQ4NTUwMg==,size_16,color_FFFFFF,t_70'>

<img name='history-feedback' src='https://img-blog.csdnimg.cn/20200612114143638.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQ4NTUwMg==,size_16,color_FFFFFF,t_70'>

<img name='my_posts' src='https://img-blog.csdnimg.cn/20200612114143590.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQ4NTUwMg==,size_16,color_FFFFFF,t_70'>
</p>

---

### <font color=#ca0c16>前端技术使用

    - nuxt
    - koa
    - vue
    - vuex
    - tinymce
    - mavon-editor
    - cookie-universal-nuxt
    - cookieparser
    - element-ui
    - VueParticles
    - nuxtjs/router
    - vue-cli3
    - axios
    - nprogres
    - crypto-js
    - vue-infinite-scroll
    - qiniu-js
    - vue-star

---

### <font color=#ca0c16>后端技术使用

    - django
    - django restframe work
    - django-channels
    - celery
    - django-mptt
    - django-debug-toolbar
    - daphne
    - concurrent-log-handler
    - django-filter
    - cryptography
    - qiniu
---

### <font color=#ca0c16>关系型数据库选型

    - mysql

---

### <font color=#ca0c16>非关系型数据库选型

    - redis

---

### <font color=#ca0c16>项目运行

_celery部分:_

```
# linux|macos:
celery -B -A sheep.celery worker -l info

# windows:
# 定时任务:
celery -A sheep.celery beat
# 新打开cmd窗口,异步任务
celery -A sheep.celery worker -l info --pool=eventlet
```

_后台部分:_

```
cd sheep
# 安装django依赖
pip3 install -r requirements.txt
# 生成数据库迁移文件
python manage.py makemigrations
# 执行迁移文件
python manage.py migrate

# 测试环境运行
python manage.py runserver
# 线上环境运行
daphne sheep.asgi:application

# 有什么自定义覆盖的配置在settings.py文件旁新建local_setting.py文件进行重新变量定义就ok
# settings.py同级目录下有local_setting_example.py文件作为样板,本地配置参考这里
```

_前端部分:_

```
# 开发环境:
cd sheep-nuxt
npm install
npm run dev

# 正式环境:
cd sheep-nuxt
npm install
npm run build
npm run start
```

#
