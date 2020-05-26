from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.post.models import User
from utils.models import BaseModel
from sheep import settings
# Create your models here.


class UploadHistoryModel(BaseModel):
    user_id = models.IntegerField(verbose_name='创建人', null=False)
    url = models.FileField(verbose_name='上传地址', null=False)

    def __str__(self):
        return f'{self.user_id}:{self.url}'

    class Meta:
        verbose_name_plural = verbose_name = '上传文件历史表'
        ordering = ('-created_time',)


class FeedbackCategory(BaseModel, MPTTModel):
    """帖子分类表"""
    name = models.CharField(max_length=128, null=False, verbose_name='反馈分类')
    desc = models.CharField(max_length=512, null=True, verbose_name='反馈简介')
    author_id = models.IntegerField(null=False, verbose_name='创建人', db_index=True)
    image = models.URLField(null=True, verbose_name='分类ICON')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children',
                            verbose_name='父亲ID', null=True, blank=True)

    @classmethod
    def create_default_category(cls):
        """创建默认反馈类别"""
        categorys = [
            {'name': 'python'},
            {'name': 'javaScript'},
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
        verbose_name_plural = verbose_name = '反馈类别表'
        unique_together = ('name', 'is_active',)
        ordering = ('-created_time',)

    def __str__(self):
        return self.name


class Feedback(BaseModel):
    name = models.CharField(max_length=128, null=False, verbose_name='反馈标题')
    category = models.IntegerField(null=False, default=1, verbose_name='反馈类别', db_index=True)
    desc = models.TextField(null=False, verbose_name='反馈内容')
    author_id = models.IntegerField(null=False, verbose_name='创建人', db_index=True)
    reply = models.CharField(max_length=256, null=True, verbose_name='回复内容')
    reply_author_id = models.IntegerField(null=True, verbose_name='回复人id', db_index=True)

    class Meta:
        verbose_name_plural = verbose_name = '意见反馈表'
        unique_together = ('name', 'is_active',)
        ordering = ('-created_time',)

    def __str__(self):
        return self.name