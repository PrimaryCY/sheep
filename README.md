# <font color=#ca0c16> Sheep 博客系统

**django+vue+channels 实时在线聊天博客系统**
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

- 登录注册
- 发表文章(支持富文本+markdown)
- 个人资料修改
- 上传文件/图片

**_未完成:_**

- 博客删改查
- 我的收藏
- 点赞系统
- 好友关注系统
- 意见反馈
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

</p>

---

### <font color=#ca0c16>前端技术使用

    - vue
    - vuex
    - tinymce
    - mavon-editor
    - vue-cookies
    - element-ui
    - VueParticles
    - vue-router
    - vue-cli3
    - axios

---

### <font color=#ca0c16>后端技术使用

    - django
    - django restframe work
    - django-channels
    - celery
    - django-mptt
    - django-debug-toolbar

---

### <font color=#ca0c16>关系型数据库选型

    - mysql

---

### <font color=#ca0c16>非关系型数据库选型

    - redis

---

### <font color=#ca0c16>项目运行

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

# 有什么自定义覆盖的配置在settings.py文件旁新建local_settings.py文件进行重新变量定义就ok
```

_前端部分:_

```
cd c_chat
npm install
npm run serve
```

#
