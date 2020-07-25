# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/3/30 19:00
from typing import Iterable

from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import BaseManager

from utils.django_util.signals import pre_ud_save, aft_ud_save


class CustomQuerySet(QuerySet):

    def update(self, **kwargs):
        pre_ud_save.send(sender=self.model, queryset=self)
        rows = super(CustomQuerySet, self).update(**kwargs)
        aft_ud_save.send(sender=self.model, queryset=self, rows=rows)
        return rows


class Manager(BaseManager.from_queryset(CustomQuerySet)):
    pass


class BaseModelMange(Manager):

    def all(self):
        return self.filter().all()

    def filter(self, *args, **kwargs):
        fields = {i.name for i in self.model._meta.fields}
        if 'is_active' in fields and not kwargs.get('is_active'):
            kwargs['is_active'] = True
        elif 'status' in fields and not kwargs.get('status'):
            kwargs['status'] = 0
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
