from django.db import models
from mptt.models import MPTTModel

from apps.post.models import User
from utils.models import BaseModel
from sheep import settings
# Create your models here.
from utils.tools import stdout
from sheep.init_server import init_stdout


class UploadHistoryModel(BaseModel):
    user_id = models.IntegerField(verbose_name='创建人', null=False)
    url = models.FileField(verbose_name='上传地址', null=False)

    def __str__(self):
        return f'{self.user_id}:{self.url}'

    class Meta:
        verbose_name_plural = verbose_name = '上传文件历史表'
        ordering = ('-created_time',)


class FeedbackCategory(BaseModel):
    """帖子分类表"""
    name = models.CharField(max_length=128, null=False, verbose_name='反馈分类')
    desc = models.CharField(max_length=512, null=True, verbose_name='反馈简介')
    author_id = models.IntegerField(null=False, verbose_name='创建人', db_index=True)
    order = models.SmallIntegerField(null=False, verbose_name='顺序', db_index=True)

    @classmethod
    @init_stdout('feedback category')
    def create_default_category(cls):
        """创建默认反馈类别"""
        categorys = [
            {'name': '功能异常不可用', 'order': 0},
            {'name': '页面崩溃打不开', 'order': 1},
            {'name': '出现广告', 'order': 2},
            {'name': '出现敏感内容', 'order': 3},
            {'name': '其它', 'order': 4},
        ]
        author = User.objects.filter(phone__in=settings.ADMIN_PHONE).only('id').first()
        if not author:
            return
        author_id = author.id
        data_list = []
        for cat in categorys:
            if cls.objects.filter(name=cat['name']).first():
                continue
            data_list.append(cls(name=cat['name'], author_id=author_id, order=cat['order']))
        cls.objects.bulk_create(data_list)

    class Meta:
        verbose_name_plural = verbose_name = '反馈类别表'
        unique_together = ('name', 'is_active',)
        ordering = ('order',)

    def __str__(self):
        return self.name


class Feedback(BaseModel):
    # name = models.CharField(max_length=128, null=False, verbose_name='反馈标题', db_index=True)
    category_id = models.IntegerField(null=False, default=1, verbose_name='反馈类别', db_index=True)
    html_content = models.CharField(max_length=3000, null=False, verbose_name='反馈html内容')
    content = models.CharField(max_length=1024, null=False, verbose_name='反馈内容')
    contact_way = models.CharField(max_length=30, null=False, verbose_name='联系方式')
    author_id = models.IntegerField(null=False, verbose_name='创建人', db_index=True)
    reply = models.CharField(max_length=256, null=True, verbose_name='回复内容')
    reply_author_id = models.IntegerField(null=True, verbose_name='回复人id', db_index=True)
    reply_time = models.DateTimeField(null=True, verbose_name='回复时间')

    class Meta:
        verbose_name_plural = verbose_name = '意见反馈表'
        ordering = ('-created_time',)

    def __str__(self):
        return self.contact_way