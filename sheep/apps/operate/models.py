from django.db import models
from django.db.models import F

from apps.post.models import Post
from apps.post.serializer import PostSerializer
from utils.django_util.models import BaseModel

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
    user_id = models.PositiveIntegerField(verbose_name='用户id', db_index=True)
    name = models.CharField(max_length=128, verbose_name='收藏类别名称')
    desc = models.CharField(max_length=512, verbose_name='收藏类别描述')
    is_show = models.BooleanField(default=True, verbose_name='是否展示')
    resource_num = models.PositiveIntegerField(default=0, verbose_name='收藏资源数量')

    class Meta:
        verbose_name_plural = verbose_name = '用户收藏帖子类别表'
        ordering = ('-update_time', '-created_time',)

    def __str__(self):
        return self.name


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
    def add_or_del_like_num(cls, collect):
        """
        对type对应的资源增加或删除收藏数量
        :param collect: 实例
        :return:
        """
        model = cls.TYPE_MODEL[collect.type]
        if collect.is_active:
            return model.objects.filter(id=collect.resource_id).update(like_num=F('like_num')+1)
        model.objects.filter(id=collect.resource_id).update(like_num=F('like_num')-1)

    @classmethod
    def select_is_like(cls, user_id: int, type: int, resource_id: int):
        """
        用户是否已经收藏
        :param user_id: 用户Id
        :param type: 类型
        :param resource_id:
        :return: bool
        """
        res = cls.objects.filter(user_id=user_id, type=type, resource_id=resource_id).only('id').first()
        return bool(res)

    class Meta:
        verbose_name_plural = verbose_name = '用户收藏资源详情表'
        ordering = ('-update_time', '-created_time')

    def __str__(self):
        return self.resource_id


class Praise(BaseModel):
    """点赞表"""
    TYPE_CHOICES = TYPE_CHOICES_MAPPING
    TYPE_MODEL = TYPE_MODEL_MAPPING

    user_id = models.PositiveIntegerField(db_index=True, verbose_name='用户')
    resource_id = models.PositiveSmallIntegerField(db_index=True, verbose_name='资源id')
    type = models.PositiveSmallIntegerField(db_index=True, choices=TYPE_CHOICES, verbose_name='点赞资源类型')

    @classmethod
    def add_or_del_praise_num(cls, praise):
        """
        对type对应的资源增加或删除点赞数
        :param praise: 类实例
        :return:
        """
        model = cls.TYPE_MODEL[praise.type]
        if praise.is_active:
            return model.objects.filter(id=praise.resource_id).update(like_num=F('like_num') + 1)
        model.objects.filter(id=praise.resource_id).update(like_num=F('like_num') - 1)

    @classmethod
    def select_is_praise(cls, user_id: int, type: int, resource_id: int):
        """
        查看用户是否点赞过
        :param user_id: 用户id
        :param type: 类型
        :param resource_id: 资源id
        :return: bool
        """
        res = cls.objects.filter(user_id=user_id, type=type, resource_id=resource_id).only('id').first()
        return bool(res)

    class Meta:
        verbose_name_plural = verbose_name = '用户点赞表'
        ordering = ('-update_time', '-created_time')

    def __str__(self):
        return self.resource_id


class Focus(BaseModel):
    """用户关注"""
    user_id = models.PositiveIntegerField(db_index=True, verbose_name='用户')
    focus_id = models.PositiveIntegerField(db_index=True, verbose_name='关注人')

    class Meta:
        verbose_name_plural = verbose_name = '用户关注表'
        ordering = ('-update_time', '-created_time')

    def __str__(self):
        return self.user_id
