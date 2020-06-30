from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from utils.models import BaseModel
from sheep import settings
from sheep.init_server import init_stdout

User = get_user_model()


class Category(BaseModel, MPTTModel):
    """帖子分类表"""
    name = models.CharField(max_length=128, null=False, verbose_name='帖子分类')
    desc = models.CharField(max_length=512, null=True, verbose_name='分类简介')
    author_id = models.IntegerField(null=False, verbose_name='创建人', db_index=True)
    image = models.URLField(null=True, verbose_name='分类ICON')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children',
                            verbose_name='父亲ID', null=True, blank=True)

    @property
    def child(self):
        """显示所有的子节点"""
        tree = self.get_descendants().values("id", "name", "parent_id", "level", "desc", 'author_id', 'image', 'parent__name').iterator()
        init = {}
        for i in tree:
            init[i['id']] = i
            i.setdefault('child', [])
        res = []
        for k, v in init.items():
            if v.get('parent_id') != self.id:
                init[v['parent_id']]['child'].append(v)
            else:
                res.append(v)
            del k, v

        # 删除所有空child,外层的空child置为None
        if not init:
            return None
        for k, v in init.items():
            if not v['child']:
                v['child'] = None
        return res

    @classmethod
    @init_stdout('post category')
    def create_default_category(cls):
        """创建默认文章类别"""
        categorys = [
            {'name': 'python'},
            {'name': 'javaScript'},
            {'name': 'java'},
            {'name': 'go'},
            {'name': '前端'},
            {'name': '数据库', 'child':[
                {
                    'name': 'mysql'
                }, {
                    'name': 'redis'
                }, {
                    'name': '其它'
                }
                ]
            },
            {'name': '运维'},
            {'name': '游戏'},
            {'name': 'elasticSearch'},
            {'name': '其它'}
        ]
        author = User.objects.filter(phone__in=settings.ADMIN_PHONE).only('id').first()
        if not author:
            return
        author_id = author.id

        def _execute(c_list, parent_id=None):
            for category in c_list:
                if cls.objects.filter(name=category['name']).first():
                    continue
                cls.objects.create(name=category['name'], author_id=author_id, parent_id=parent_id)
                if not category.get('child'):
                    continue
                parent = cls.objects.filter(name=category['name']).first().id
                _execute(category['child'], parent_id=parent)
        _execute(categorys)

    class Meta:
        verbose_name_plural = verbose_name = '帖子分类表'
        unique_together = ('name', 'is_active',)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Post(BaseModel):
    """帖子表"""
    content_type_choices = (
        (1, '富文本'),
        (2, 'markdown')
    )
    post_type_choices = (
        (1, '文章'),
        (2, '问题')
    )

    name = models.CharField(max_length=128, null=False, verbose_name='帖子标题')
    author_id = models.IntegerField(null=False, verbose_name='创建人', db_index=True)
    category = models.IntegerField(null=False, default=1, verbose_name='帖子分类', db_index=True)
    # desc = models.CharField(max_length=512, null=True, verbose_name='帖子简介')
    html_content = models.TextField(null=False, verbose_name='html帖子内容')
    content = models.TextField(null=False, verbose_name='帖子内容')
    post_type = models.SmallIntegerField(choices=post_type_choices, default=1, verbose_name='文章类型')
    image = models.URLField(null=True, verbose_name='帖子封面')
    post_num = models.IntegerField(null=False, default=0, verbose_name='评论数量')
    read_num = models.IntegerField(default=0, verbose_name='阅读数量')
    like_num = models.IntegerField(default=0, verbose_name='收藏数量')
    praise_num = models.IntegerField(default=0, verbose_name='点赞数量')
    # not_reply = models.BooleanField(default=True, verbose_name='是否可以回复')
    content_type = models.SmallIntegerField(choices=content_type_choices,verbose_name='内容类型')

    @classmethod
    def get_simple_post_info(cls, post_id: int):
        """
        获取简单的帖子信息
        :param post_id:
        :return:
        """
        return cls.objects.filter(id=post_id).values(*cls.exclude(['content']))

    @classmethod
    def add_post_num(cls, post_id: int):
        """
        增加评论数量
        :param post_id:帖子id
        :return:
        """
        cls.objects.filter(id=post_id).update(post_num=F('post_num')+1)
        return post_id

    @classmethod
    def del_post_num(cls, post_id: int):
        """
        减少评论数量
        :param post_id:帖子id
        :return:
        """
        cls.objects.filter(id=post_id).update(post_num=F('post_num')-1)
        return post_id

    @classmethod
    def add_read_num(cls, post_id: int):
        """
        增加阅读数量
        :return:
        """
        return cls.objects.filter(id=post_id).update(read_num=F('read_num')+1)

    @classmethod
    def get_banner(cls):
        """
        获取banner数据,默认获取点赞数最多同时有封面的5条
        :return:
        """
        return list(cls.objects.filter(image__isnull=False).order_by('praise_num').values('id', 'image', 'name')[:5])

    class Meta:
        verbose_name_plural = verbose_name = '帖子表'
        unique_together = ('name', 'is_active',)
        ordering = ('-created_time',)

    def __str__(self):
        return self.name


class PostReply(BaseModel, MPTTModel):
    """帖子评论表"""
    content = models.TextField(verbose_name='评论', null=False)
    praise_num = models.IntegerField(default=0, verbose_name='点赞数量')
    author_id = models.IntegerField(null=False, verbose_name='创建人', db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='child',
                            verbose_name='父评论', null=True, blank=True)
    post_id = models.IntegerField(verbose_name='帖子id', null=False, db_index=True)
    replier_id = models.IntegerField(null=True, verbose_name='回复人id', db_index=True)

    def is_del(self, user_id):
        """用户是否可以删除该回复"""
        return self.author_id == user_id and self.get_descendant_count() <= 0

    class Meta:
        verbose_name_plural = verbose_name = '帖子评论表'

    def __str__(self):
        return self.content
