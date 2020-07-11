# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/11 21:01
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor

from .bits import LimitOffsetPaginationKeyBit


class LimitOffsetListKeyConstructor(DefaultKeyConstructor):
    list_sql_query = bits.ListSqlQueryKeyBit()
    pagination = LimitOffsetPaginationKeyBit()