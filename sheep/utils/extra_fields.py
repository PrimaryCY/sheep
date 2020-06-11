# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/6 21:08
from collections import OrderedDict
from typing import Iterator, Any, Iterable

from rest_framework import fields
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, Field
from rest_framework.serializers import SerializerMethodField


class CurrentUserIdDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.id

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class RangeField(fields.Field):
    """给定一个范围,使前端传参必须在此范围内的字段"""
    default_error_messages = {
        'notIn': '不在此范围内!',
    }

    def __init__(self, iterable: list, *args, **kwargs):
        assert isinstance(iterable, Iterable), (
            f'RangeField应该传入一个可迭代对象!'
        )
        self.iterable = iterable

        if kwargs.get('error_messages'):
            self.default_error_messages['notIn'] = kwargs.pop('error_messages')

        self.data_type = kwargs.pop('data_type', str)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data: Any):
        try:
            data = self.data_type(data)
        except:
            self.fail('notIn')

        if data not in self.iterable:
            self.fail('notIn')
        return data

    def to_representation(self, value):
        return value


class CustomChoiceFiled(ChoiceField):

    def to_representation(self, value):
        return self.choices.get(value)


class SerializerMethodAndWriteField(SerializerMethodField):
    """
    serializerMethod支持write操作
    """
    def __init__(self, method_name=None, source=None, **kwargs):
        self.method_name = method_name
        # 想要新增一个不存在的字段名称需要手动指定source
        self.source = source
        super(SerializerMethodField, self).__init__(**kwargs)

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value)

    def to_internal_value(self, data: Any):
        return data

