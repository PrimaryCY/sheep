# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/3/30 19:00
from typing import Iterable

from django.db import models


class BaseModelMange(models.Manager):

    def all(self):
        return self.filter(is_active=True).all()

    def filter(self, *args, **kwargs):
        if not kwargs.get('is_active'):
            kwargs['is_active'] = True
        return super().filter(*args, **kwargs)


class BaseModel(models.Model):
    """基本model"""
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    is_active = models.BooleanField(default=True, verbose_name='状态')
    objects = BaseModelMange()
    raw_objects = models.Manager()

    @classmethod
    def exclude(cls, *args: Iterable) -> list:
        """
        配合model.objects.values(*exclude('name'))使用,去除不需要的字段
        :param args: iterable
        :return: list
        """
        return [f.name for f in cls._meta.fields if f.name not in args]

    class Meta:
        abstract = True