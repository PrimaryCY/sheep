# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/9/7 19:34
import datetime

import django_filters
from django_filters.rest_framework import FilterSet


class BaseFilterSet(FilterSet):
    start_update_time = django_filters.DateFilter(field_name='update_time', lookup_expr='gte', label='开始创建')
    end_update_time = django_filters.DateFilter(field_name='update_time', lookup_expr='lte',
                                                method='filter_end_update_time', label='结束创建')
    start_created_time = django_filters.DateFilter(field_name='created_time', lookup_expr='gte', label='开始创建')
    end_created_time = django_filters.DateFilter(field_name='created_time', lookup_expr='lte',
                                                 method='filter_end_created_time', label='结束创建')

    def filter_end_created_time(self, qs, name, value):
        return qs.filter(update_time__lte=value + datetime.timedelta(days=1))

    def filter_end_update_time(self, qs, name, value):
        return qs.filter(update_time__lte=value + datetime.timedelta(days=1))
