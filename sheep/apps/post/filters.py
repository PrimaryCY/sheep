# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/5/22 17:01
from django_filters.rest_framework import FilterSet
import django_filters


class PostFilter(FilterSet):
    start_created_time = django_filters.DateFilter(field_name='created_time', lookup_expr='gte', label='开始创建')
    end_created_time = django_filters.DateFilter(field_name='created_time', lookup_expr='lte', label='结束创建')
    category = django_filters.NumberFilter(field_name='category')
