import re
from datetime import datetime
from typing import Iterable

from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
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
            {'id': 1, 'name': '历史', 'child': [
                {
                    'id': 9,
                    'name': '先秦'
                },
                {
                    'id': 10,
                    'name': '秦汉三国'
                },
                {
                    'id': 11,
                    'name': '两晋隋唐'
                },
                {
                    'id': 12,
                    'name': '两宋元明'
                },
                {
                    'id': 13,
                    'name': '清史民国'
                },
                {
                    'id': 14,
                    'name': '罗马'
                },
                {
                    'id': 15,
                    'name': '中世纪'
                },
                {
                    'id': 16,
                    'name': '文艺复兴'
                },
                {
                    'id': 17,
                    'name': '工业革命'
                },
                {
                    'id': 18,
                    'name': '维多利亚'
                },
                {
                    'id': 19,
                    'name': '第二次世界大战'
                },
            ]},
            {'id': 2, 'name': '游戏', 'child': [
                {
                    'id': 20,
                    'name': 'Paradox'
                },
                {
                    'id': 21,
                    'name': '光荣株式会社'
                },
                {
                    'id': 22,
                    'name': '2K'
                },
                {
                    'id': 23,
                    'name': 'CD Projekt'
                },
                {
                    'id': 24,
                    'name': 'Dota'
                },
                {
                    'id': 25,
                    'name': 'Play station'
                },
                {
                    'id': 26,
                    'name': 'Nintendo switch'
                }
            ]},
            {'id': 3, 'name': '旅游', 'child': [
                {
                    'id': 27,
                    'name': '求伴'
                },
                {
                    'id': 28,
                    'name': '北京'
                },
                {
                    'id': 29,
                    'name': '西安'
                },
                {
                    'id': 30,
                    'name': '成都'
                },
                {
                    'id': 31,
                    'name': '上海'
                },
                {
                    'id': 32,
                    'name': '南京'
                },
                {
                    'id': 33,
                    'name': '其它城市'
                }
            ]},
            {'id': 4, 'name': '生活', 'child': [
                {
                    'id': 34,
                    'name': '电影'
                },
                {
                    'id': 35,
                    'name': '火锅'
                },
                {
                    'id': 36,
                    'name': '烤肉'
                },
                {
                    'id': 37,
                    'name': '面条'
                },
                {
                    'id': 38,
                    'name': '烤鱼'
                },
                {
                    'id': 39,
                    'name': '唱歌'
                },
                {
                    'id': 40,
                    'name': '小酒小烟'
                },
            ]},
            {'id': 5, 'name': '创意', 'child': [
                {
                    'id': 41,
                    'name': '奇思妙想'
                },
                {
                    'id': 42,
                    'name': '分享创造'
                }
            ]},
            {'id': 6, 'name': '程序', 'child': [
                {
                    'id': 43,
                    'name': 'go'
                },
                {
                    'id': 44,
                    'name': 'python'
                },
                {
                    'id': 45,
                    'name': 'javaScript'
                },
                {
                    'id': 46,
                    'name': 'mysql'
                },
                {
                    'id': 47,
                    'name': 'redis'
                },
                {
                    'id': 48,
                    'name': 'vue'
                },
                {
                    'id': 49,
                    'name': 'elasticSearch'
                },
                {
                    'id': 50,
                    'name': '运维'
                },
            ]},
            {'id': 7, 'name': 'OS', 'child': [
                {
                    'id': 51,
                    'name': 'Centos'
                },
                {
                    'id': 52,
                    'name': 'Ubuntu'
                },
                {
                    'id': 53,
                    'name': 'Debian'
                },
                {
                    'id': 54,
                    'name': 'Fedora'
                },
                {
                    'id': 55,
                    'name': 'SUSE'
                },
                {
                    'id': 56,
                    'name': 'mac'
                },
                {
                    'id': 57,
                    'name': 'windows'
                }
            ]},
            {'id': 8, 'name': '羊村', 'child': [
                {
                    'id': 58,
                    'name': '育羊心得'
                },
                {
                    'id': 59,
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
                                                                      'name': category.get('name'),
                                                                      'order': category.get('order', 0)},
                                                            id=category['id'],
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
        fields = ['name', 'author_id', 'category',
                  'image', 'post_type', 'desc']
        return Post.raw_objects.filter(id=post_id).values(*fields).first()

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


class Sensitive(models.Model):
    key_word = models.CharField(max_length=32, verbose_name='关键字')
    con = settings.DEFAULT_REDIS

    class Meta:
        verbose_name_plural = verbose_name = '敏感词过滤表'

    CACHE_KEY = 'key_word'

    @classmethod
    def filter_key_word(cls, text: str):
        """
        敏感词过滤
        :param text:
        :return: flag(是否包含敏感词), key_word
        """
        cache_key_word = cls.con.get(cls.CACHE_KEY)
        if cache_key_word:
            key_word = cache_key_word
        else:
            key_word = cls.objects.values_list('key_word', flat=True)
            key_word = '|'.join(key_word)
            # 缓存keyword时常为10分钟
            cls.con.set(cls.CACHE_KEY, key_word, ex=60 * 10)
        res = re.search(key_word, text)
        if not res:
            return False, None
        return True, res.group()

    @classmethod
    def delete_cache(cls):
        """
        清楚缓存
        :return:
        """
        return cls.con.delete(cls.CACHE_KEY)
