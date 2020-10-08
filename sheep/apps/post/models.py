from collections import defaultdict
from datetime import datetime
from typing import Iterable

from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from utils.django_util.models import BaseModel
from sheep import settings
from sheep.init_server import init_stdout

User = get_user_model()


class Category(MPTTModel, BaseModel):
    """帖子分类表"""
    name = models.CharField(max_length=128, null=False, verbose_name='帖子分类')
    desc = models.CharField(max_length=512, null=True, verbose_name='分类简介')
    author_id = models.IntegerField(null=False, verbose_name='创建人', db_index=True)
    # image = models.URLField(null=True, verbose_name='分类ICON')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children',
                            verbose_name='父亲ID', null=True, blank=True)
    order = models.SmallIntegerField(default=0, verbose_name='排序', db_index=True)

    @property
    def child(self):
        """显示所有的子节点"""
        tree = self.get_descendants().values("id", "name", "parent_id", "level", "desc", 'author_id',
                                             'parent__name').order_by('order', 'id').iterator()
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
        categories = [
            {'name': '历史', 'child': [
                {
                    'name': '先秦'
                },
                {
                    'name': '秦汉三国'
                },
                {
                    'name': '两晋隋唐'
                },
                {
                    'name': '两宋元明'
                },
                {
                    'name': '清史民国'
                },
                {
                    'name': '罗马'
                },
                {
                    'name': '中世纪'
                },
                {
                    'name': '文艺复兴'
                },
                {
                    'name': '工业革命'
                },
                {
                    'name': '维多利亚'
                },
                {
                    'name': '第二次世界大战'
                },
            ]},
            {'name': '游戏', 'child': [
                {
                    'name': 'Paradox'
                },
                {
                    'name': '光荣株式会社'
                },
                {
                    'name': '2K'
                },
                {
                    'name': 'CD Projekt'
                },
                {
                    'name': 'Dota'
                },
                {
                    'name': 'Play station'
                },
                {
                    'name': 'Nintendo switch'
                }
            ]},
            {'name': '旅游', 'child': [
                {
                    'name': '求伴'
                },
                {
                    'name': '北京'
                },
                {
                    'name': '西安'
                },
                {
                    'name': '成都'
                },
                {
                    'name': '上海'
                },
                {
                    'name': '南京'
                },
                {
                    'name': '其它城市'
                }
            ]},
            {'name': '生活', 'child': [
                {
                    'name': '电影'
                },
                {
                    'name': '火锅'
                },
                {
                    'name': '烤肉'
                },
                {
                    'name': '面条'
                },
                {
                    'name': '烤鱼'
                },
                {
                    'name': '唱歌'
                },
                {
                    'name': '小酒小烟'
                },
            ]},
            {'name': '创意', 'child': [
                {
                    'name': '奇思妙想'
                },
                {
                    'name': '分享创造'
                }
            ]},
            {'name': '程序', 'child': [
                {
                    'name': 'go'
                },
                {
                    'name': 'python'
                },
                {
                    'name': 'javaScript'
                },
                {
                    'name': 'mysql'
                },
                {
                    'name': 'redis'
                },
                {
                    'name': 'vue'
                },
                {
                    'name': 'elasticSearch'
                },
                {
                    'name': '运维'
                },
            ]},
            {'name': 'OS', 'child': [
                {
                    'name': 'Centos'
                },
                {
                    'name': 'Ubuntu'
                },
                {
                    'name': 'Debian'
                },
                {
                    'name': 'Fedora'
                },
                {
                    'name': 'SUSE'
                },
                {
                    'name': 'mac'
                },
                {
                    'name': 'windows'
                }
            ]},
            {'name': '羊村', 'child': [
                {
                    'name': '育羊心得'
                },
                {
                    'name': '羊圈'
                }
            ]}
        ]
        author = User.objects.filter(phone__in=settings.ADMIN_PHONE).only('id').first()
        if not author:
            return
        author_id = author.id

        def _execute(c_list, parent_id=None):
            for category in c_list:
                obj, created = cls.objects.update_or_create(defaults={'author_id': author_id,
                                                                      'order': category.get('order', 0)},
                                                            name=category['name'],
                                                            parent_id=parent_id)
                if not category.get('child'):
                    continue
                _execute(category['child'], parent_id=obj.id)

        _execute(categories)

    class Meta:
        verbose_name_plural = verbose_name = '帖子分类表'
        # unique_together = ('name', 'is_active',)

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
    post_status_choices = (
        (0, '上线'),
        (1, '用户删除'),
        (2, '管理员删除'),
        (3, '点赞数过低删除'),
        (4, '内容违规')
    )

    name = models.CharField(max_length=128, null=False, verbose_name='帖子标题')
    author_id = models.IntegerField(null=False, verbose_name='创建人', db_index=True)
    category = models.IntegerField(null=False, default=1, verbose_name='帖子分类', db_index=True)
    desc = models.CharField(max_length=512, default='', verbose_name='帖子简介')
    html_content = models.TextField(null=False, verbose_name='html帖子内容')
    content = models.TextField(null=False, verbose_name='帖子内容')
    post_type = models.SmallIntegerField(choices=post_type_choices, default=1, verbose_name='文章类型')
    image = models.URLField(null=True, verbose_name='帖子封面')
    post_num = models.IntegerField(null=False, default=0, verbose_name='评论数量')
    read_num = models.IntegerField(default=0, verbose_name='阅读数量')
    like_num = models.IntegerField(default=0, verbose_name='收藏数量')
    praise_num = models.IntegerField(default=0, verbose_name='点赞数量')
    # not_reply = models.BooleanField(default=True, verbose_name='是否可以回复')
    content_type = models.SmallIntegerField(choices=content_type_choices, verbose_name='内容类型')
    newest_user_id = models.IntegerField(null=True, verbose_name='最新回复人')
    newest_time = models.DateTimeField(null=True, verbose_name='回复时间')
    status = models.PositiveSmallIntegerField(choices=post_status_choices, null=False, default=0,
                                              verbose_name='文章上下线状态')
    is_active = None

    @classmethod
    def get_simple_post_info(cls, post_id: int):
        """
        获取简单的帖子信息
        :param post_id:
        :return:
        """
        return cls.objects.filter(id=post_id).values(*cls.exclude('content'))

    @classmethod
    def bulk_get_simple_post_info(cls, ids: Iterable):
        """
        批量获取简单的帖子信息
        :param ids:
        :return:
        """
        return {i['id']: i for i in cls.objects.filter(id__in=ids).values(*cls.exclude('content', 'html_content'))}

    @classmethod
    def add_post_num(cls, post_id: int, newest_user_id: int):
        """
        增加评论数量,修改最后评论人
        :param post_id:帖子id
        :param newest_user_id:回复人id
        :return:
        """
        cls.objects.filter(id=post_id).update(post_num=F('post_num') + 1,
                                              newest_time=datetime.now(),
                                              newest_user_id=newest_user_id)
        return post_id

    @classmethod
    def del_post_num(cls, post_id: int):
        """
        减少评论数量,修改最后评论id
        :param post_id:帖子id
        :return:
        """
        reply = PostReply.objects.filter(post_id=post_id, parent__isnull=True, is_active=True).only("author_id",
                                                                                                    "created_time").first()
        if reply:
            cls.objects.filter(id=post_id).update(post_num=F('post_num') - 1,
                                                  newest_time=reply.created_time,
                                                  newest_user_id=reply.author_id)
        else:
            cls.objects.filter(id=post_id).update(post_num=F('post_num') - 1,
                                                  newest_time=None,
                                                  newest_user_id=None)
        return post_id

    @classmethod
    def add_read_num(cls, post_id: int):
        """
        增加阅读数量
        :return:
        """
        return cls.objects.filter(id=post_id).update(read_num=F('read_num') + 1)

    class Meta:
        verbose_name_plural = verbose_name = '文章/问题表'
        unique_together = ('status', 'name')
        ordering = ('-created_time',)

    def __str__(self):
        return self.name


class PostReply(BaseModel, MPTTModel):
    """帖子评论表"""
    content = models.TextField(verbose_name='评论', null=False)
    html_content = models.TextField(verbose_name='评论', null=False)
    praise_num = models.IntegerField(default=0, verbose_name='点赞数量')
    author_id = models.IntegerField(null=False, verbose_name='创建人', db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='child',
                            verbose_name='父评论', null=True, blank=True)
    post_id = models.IntegerField(verbose_name='帖子id', null=False, db_index=True)
    replier_id = models.IntegerField(null=True, verbose_name='回复人id', db_index=True)
    is_read = models.BooleanField(default=False, verbose_name='是否已读')

    def is_del(self, user_id):
        """
        用户是否可以删除该回复
        :param user_id:
        :return: 0 不可以删除  1 不可以删除，有子评论  2可以删除
        """
        if not self.author_id == user_id:
            return 0
        elif not PostReply.objects.filter(parent_id=self.id, is_active=True).exists():
            return 2
        else:
            return 1
        # return self.author_id == user_id and self.get_descendant_count() <= 0

    class Meta:
        verbose_name_plural = verbose_name = '帖子评论表'
        ordering = ('-created_time', 'praise_num')

    def __str__(self):
        return self.content
