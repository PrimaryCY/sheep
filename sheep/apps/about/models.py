from django.db import models

from sheep.init_server import init_stdout
from utils.django_util.models import BaseModel


class About(BaseModel):
    content = models.TextField(null=True, verbose_name='关于我们')

    @classmethod
    @init_stdout('init about')
    def create_default_about(cls):
        """创建默认关于"""
        obj = cls.objects.first()
        if obj:
            return
        content = '关于我们'
        cls.objects.create(content=content)

    class Meta:
        verbose_name_plural = verbose_name = '关于我们'
        ordering = ('-created_time',)
