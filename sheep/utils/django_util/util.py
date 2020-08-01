# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/29 11:56
from typing import Iterable

from django.db.models import Model


def field_sort_queryset(model, items:Iterable, sort_field: str = 'id'):
    """
    field排序
    :param model:
    :param items:
    :param sort_field:
    :return:
    """
    assert issubclass(model, Model), (
        '传入的不是ModelClass'
    )
    queryset = []
    if items:
        sku_ids = ','.join([str(i) for i in items])
        field_sql = f"FIELD(`{sort_field}`,{sku_ids})"
        queryset = model.objects.extra(select={'field_sql': field_sql}, where=[f'id IN ({sku_ids})'],
                                       order_by=['field_sql'])
    return queryset


def raw_sort_queryset(model, items: Iterable):
    """
       field排序
       :param model:
       :param items:
       :param sort_field:
       :return:
    """
    assert issubclass(model, Model), (
        '传入的不是ModelClass'
    )
    queryset = model.objects.filter(id__in=items).all()
    query_dict = {i.id: i for i in queryset}
    return [query_dict[i] for i in items]
