# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/4/6 12:49
import json
import datetime
from datetime import date
from functools import wraps
from typing import Iterable

from rest_framework.pagination import LimitOffsetPagination
from rest_framework_extensions.cache.decorators import available_attrs
from rest_framework.fields import ChoiceField
from django.db.models import Model


class SetJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)





class RedisTranscaction(object):
    __slots__ = ('func',)

    def __init__(self,func):
        self.func = func

    def __call__(self,func):
        return self

    def __get__(self, instance, owner):
        @wraps(self.func,assigned=available_attrs(self.func))
        def wrap(*args,**kwargs):
            print('使用事务了')
            instance.redis= instance.redis.pipeline(transaction=True)
            instance.redis.multi()
            result=self.func(instance,*args,**kwargs)
            instance.redis.execute()
            return result
        return wrap

