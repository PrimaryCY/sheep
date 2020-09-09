import math
import random
import time
import functools
import logging
from datetime import datetime, timedelta

from django.db import models
from django.db.models import F
from django.conf import settings
from redis import ResponseError, StrictRedis
from rest_framework.exceptions import ValidationError

from apps.post.models import Post, PostReply
from apps.post.serializer import PostSerializer
from sheep.constant import RET, error_map
from utils.django_util.models import BaseModel


logger = logging.getLogger('django')
# 废弃
TYPE_CHOICES_MAPPING = (
        (1, '帖子'),
    )

TYPE_MODEL_MAPPING = {
        1: Post,
    }

TYPE_SERIALIZER_MAPPING = {
        1: PostSerializer,
    }


class CollectCategory(BaseModel):
    """收藏类别表"""
    default_images = [
        'https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vY29sbGVjdGlvbi9kZWZhdWx0LWltYWdlcy83LmpwZw?x-oss-process=image/format,png',
        'https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vY29sbGVjdGlvbi9kZWZhdWx0LWltYWdlcy81LmpwZw?x-oss-process=image/format,png',
        'https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vY29sbGVjdGlvbi9kZWZhdWx0LWltYWdlcy8xOS5qcGc?x-oss-process=image/format,png'
    ]
    user_id = models.PositiveIntegerField(verbose_name='用户id', db_index=True)
    name = models.CharField(max_length=128, verbose_name='收藏类别名称')
    image = models.URLField(null=False, verbose_name='收藏类别封面')
    desc = models.CharField(max_length=512, null=False, verbose_name='收藏类别描述')
    is_show = models.BooleanField(default=True, verbose_name='是否展示')
    total = models.PositiveIntegerField(default=0, verbose_name='总数')

    def __init__(self, *args, **kwargs):
        kwargs = self.set_default(kwargs)
        super().__init__(*args, **kwargs)

    def set_default(self, attr):
        image = attr.get('image')
        if not image:
            attr['image'] = random.choice(self.default_images)
        return attr

    class Meta:
        verbose_name_plural = verbose_name = '用户收藏帖子类别表'
        ordering = ('-created_time',)

    def __str__(self):
        return self.name


class CollectRedisModel(object):
    REDIS_KEY = 'col-u{user_id}-c{category_id}'
    TYPE = set()
    con = settings.OPERATE_REDIS

    def __init__(self, user_id, category_id):
        """生成key"""
        self._category = category_id
        self._u = user_id
        self.redis_key = self.REDIS_KEY.format(user_id=user_id,
                                               category_id=category_id)

    def create_or_delete(self, resource_id: int):
        """
        新增或删除
        :return: True  为删除
                 False 为新建
        """
        row = self.con.zrem(self.redis_key, resource_id)
        if not row:
            self.con.zadd(self.redis_key, {resource_id: int(time.time())})
            return not False
        return not True

    def get_count(self):
        """
        获取收藏集总数
        :return:
        """
        return self.con.zcard(self.redis_key)

    def get_is_like(self, resource_id):
        """
        该收藏集是否收藏了该资源
        :param resource_id: 资源id
        :return:
        """
        return bool(self.con.zscore(self.redis_key, resource_id))

    @classmethod
    def get_user_is_like(cls, user, resource_id):
        """
        该用户是否收藏了该资源
        :param user:
        :param resource_id:
        :return:
        """
        if user.is_anonymity:
            return False
        re_str = 'col-u{user_id}-*'.format(user_id=user.id)
        for key in cls.con.scan_iter(match=re_str, count=5000):
            if cls.con.zscore(key, resource_id):
                return True
        else:
            return False

    def get_all(self, request):
        """
        获取某个收藏集下全部数据
        :param request:用于过滤收藏日期
        :return:
        """
        start_collect_time = request.query_params.get('start_collect_time')
        end_collect_time = request.query_params.get('end_collect_time')
        try:
            if start_collect_time:
                start_collect_time = datetime.strptime(start_collect_time, '%Y-%m-%d')
                start_collect_time = math.floor(start_collect_time.replace().timestamp())
            if end_collect_time:
                end_collect_time = datetime.strptime(end_collect_time, '%Y-%m-%d') + \
                                   timedelta(days=1)
                end_collect_time = math.ceil(end_collect_time.replace().timestamp())
        except:
            raise ValidationError({'success': False, 'code': RET.PARAMERR, 'msg': error_map[RET.PARAMERR]})

        return {int(k): v for k, v in self.con.zrevrangebyscore(self.redis_key,
                                                                min=start_collect_time or 1,
                                                                max=end_collect_time or int(time.time()),
                                                                withscores=True,
                                                                score_cast_func=int)}

    def delete(self):
        """
        删除该收藏集下的所有内容
        备份保存三十天
        """
        post_ids = self.con.zrange(self.redis_key, 0, -1)
        Post.objects.filter(id__in=post_ids).update(like_num=F('like_num')-1)

        back_key = f'{self.redis_key}-backup'
        try:
            with self.con.pipeline() as con:
                con.rename(self.redis_key, back_key)
                con.expire(back_key, 60*60*24*30)
                con.execute()
        except ResponseError:
            pass


# 废弃
class Collect(BaseModel):
    """收藏表"""
    TYPE_CHOICES = TYPE_CHOICES_MAPPING
    # type的model映射
    TYPE_MODEL = TYPE_MODEL_MAPPING

    category_id = models.PositiveSmallIntegerField(db_index=True, verbose_name='收藏类别id')
    resource_id = models.PositiveSmallIntegerField(db_index=True, verbose_name='资源id')
    type = models.PositiveSmallIntegerField(db_index=True, choices=TYPE_CHOICES, verbose_name='资源类型')
    user_id = models.PositiveIntegerField(db_index=True, null=False, verbose_name='用户id')

    @classmethod
    def after_collect(cls, category_id, resource_id, is_active, *args, **kwargs):
        """
        用户收藏之后的操作,对相关分类,资源的收藏总数+1|-1
        :param type:
        :param category_id: 收藏集id
        :param resource_id: 资源id
        :param is_active: 是否激活
        :return:
        """
        model = Post
        if is_active:
            CollectCategory.objects.filter(id=category_id).update(total=F('total')+1)
            return model.objects.filter(id=resource_id).update(like_num=F('like_num')+1)
        CollectCategory.objects.filter(id=category_id).update(total=F('total') - 1)
        model.objects.filter(id=resource_id).update(like_num=F('like_num')-1)

    # @classmethod
    # def select_is_like(cls, user_id: int, type: int, resource_id: int):
    #     """
    #     资源是否被用户收藏
    #     :param user_id: 用户Id
    #     :param type: 类型
    #     :param resource_id:
    #     :return: bool
    #     """
    #     res = cls.objects.filter(user_id=user_id, type=type, resource_id=resource_id).only('id').first()
    #     return bool(res)

    class Meta:
        verbose_name_plural = verbose_name = '用户收藏资源详情表'
        ordering = ('-created_time',)

    def __str__(self):
        return str(self.resource_id)


class Praise(BaseModel):
    """点赞表"""
    PRAISE_OR_TRAMPLE_CHOICE = (
        (-1, 'cai'),
        (1, 'zan')
    )
    PRAISE_TYPE_CHOICE = {
        1: '文章',
        2: '回复'
    }

    PRAISE_TYPE_MODEL_MAPPING = {
        1: Post,
        2: PostReply
    }

    user_id = models.PositiveIntegerField(db_index=True, verbose_name='用户')
    resource_id = models.IntegerField(db_index=True, verbose_name='资源id')
    praise_or_trample = models.SmallIntegerField(null=False, default=1, choices=PRAISE_OR_TRAMPLE_CHOICE, verbose_name='赞或踩')
    t = models.PositiveSmallIntegerField(null=False, choices=PRAISE_TYPE_CHOICE.items(), verbose_name='资源类型', db_index=True)

    resource_praise_like = 'praise_l_{t}_{resource_id}'
    resource_praise_not_like = 'praise_nl_{t}_{resource_id}'
    con = settings.OPERATE_REDIS

    @classmethod
    def add_or_del_praise_num(cls, praise_or_trample: int, resource_id: int, user_id: int, t: int):
        from apps.operate.tasks import after_praise_or_trample

        resource_praise_like = cls.resource_praise_like.format(resource_id=resource_id, t=t)
        resource_praise_not_like = cls.resource_praise_not_like.format(resource_id=resource_id, t=t)
        p_after_praise_or_trample = functools.partial(after_praise_or_trample.delay,
                                                      user_id=user_id,
                                                      praise_or_trample=praise_or_trample,
                                                      t=t,
                                                      resource_id=resource_id)

        return_num = 0
        if praise_or_trample == 0:
            # 取消点赞
            is_prasie = cls.con.setbit(resource_praise_like, user_id, 0)
            is_not_praise = cls.con.setbit(resource_praise_not_like, user_id, 0)
            if is_prasie:
                return_num = -1
                p_after_praise_or_trample(-1)
            elif is_not_praise:
                return_num = +1
                p_after_praise_or_trample(+1)

        elif praise_or_trample == -1:
            # 踩
            is_praise = cls.con.setbit(resource_praise_like, user_id, 0)
            is_not_praise = cls.con.setbit(resource_praise_not_like, user_id, 1)
            if is_not_praise == 0:
                return_num = num = -2 if is_praise else -1
                p_after_praise_or_trample(num)

        elif praise_or_trample == 1:
            # 赞
            is_praise = cls.con.setbit(resource_praise_like, user_id, 1)
            is_not_praise = cls.con.setbit(resource_praise_not_like, user_id, 0)
            if is_praise == 0:
                return_num = num = +2 if is_not_praise else +1
                p_after_praise_or_trample(num)
        logger.info(f'add_or_del_praise_num--user_id:{user_id}')
        return return_num

    @classmethod
    def select_is_praise(cls, user_id: int, resource_id: int, t: int):
        """
        查看用户点赞状态， 1->点赞 -1->踩  0->无状态
        :param user_id: 用户id
        :param resource_id: 资源id
        :param t
        :return: int
        """
        logger.info(f'select_is_praise--user_id{user_id}')
        resource_praise_like = cls.resource_praise_like.format(resource_id=resource_id, t=t)
        resource_praise_not_like = cls.resource_praise_not_like.format(resource_id=resource_id, t=t)
        is_praise = cls.con.getbit(resource_praise_like, user_id)
        if is_praise:
            return 1

        is_not_praise = cls.con.getbit(resource_praise_not_like, user_id)
        if is_not_praise:
            return -1

        return 0

    class Meta:
        verbose_name_plural = verbose_name = '用户点赞表'
        ordering = ('-update_time', '-created_time')

    def __str__(self):
        return self.resource_id


class BrowsingHistoryRedisMode(object):
    """浏览记录model"""
    REDIS_KEY = 'his-u-{user_id}'
    con = settings.OPERATE_REDIS

    def __init__(self, user_id):
        self._u = user_id
        self.redis_key = self.REDIS_KEY.format(user_id=user_id)

    def create_history(self, resource_id):
        """
        添加浏览记录,最多保存100条浏览记录
        :param resource_id: 资源id
        :return:
        """
        with self.con.pipeline() as con:
            con.zadd(self.redis_key, {resource_id: int(time.time())})
            con.zremrangebyrank(self.redis_key, 101, -1)
            con.execute()

    def get_all(self, request):
        """
        获取用户历史浏览记录
        :param request:
        :return:
        """
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        try:
            if start_time:
                start_time = datetime.strptime(start_time, '%Y-%m-%d-%H:%M')
                start_time = math.floor(start_time.replace().timestamp())
            if end_time:
                end_time = datetime.strptime(end_time, '%Y-%m-%d-%H:%M')
                end_time = math.ceil(end_time.replace().timestamp())
        except:
            raise ValidationError({'success': False, 'code': RET.PARAMERR, 'msg': error_map[RET.PARAMERR]})

        return {int(k): v for k, v in self.con.zrevrangebyscore(self.redis_key,
                                                                min=start_time or 1,
                                                                max=end_time or int(time.time()),
                                                                withscores=True,
                                                                score_cast_func=int)}


class Focus(BaseModel):
    """用户关注"""
    user_id = models.PositiveIntegerField(db_index=True, verbose_name='用户')
    focus_id = models.PositiveIntegerField(db_index=True, verbose_name='关注人')

    class Meta:
        verbose_name_plural = verbose_name = '用户关注表'
        ordering = ('-update_time', '-created_time')

    def __str__(self):
        return self.user_id
