# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/9 10:22
import django_filters
from django_filters import FilterSet

from apps.post.models import Category


class AllPostFilter(FilterSet):
    """首页过滤器"""
    category = django_filters.NumberFilter(required=True, field_name='category',
                                           method='filter_category', label='类别')

    def filter_category(self, qs, name, value):
        qs = qs.defer('html_content', 'content')
        if value == 0:
            return qs
        else:
            c = Category.objects.filter(id=value).first()
            if not c:
                c_range = []
            else:
                c_range = c.get_descendants(include_self=True).values_list('id', flat=True)
            return qs.filter(category__in=c_range).order_by('like_num')
