# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/12 16:05
import django_filters
from django_filters import FilterSet

from apps.post.models import Category


class SearchPostFilter(FilterSet):
    """搜索过滤器"""
    post_type = django_filters.NumberFilter(required=True, field_name='post_type',
                                           method='filter_post_type', label='类别')

    def filter_post_type(self, qs, name, value):
        qs = qs.defer('html_content', 'content')
        if value == 0:
            return qs
        else:
            return qs.filter(post_type=value)
