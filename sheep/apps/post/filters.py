# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/5/22 17:01
from django_filters.rest_framework import FilterSet
import django_filters

from apps.post.models import Category


class PostFilter(FilterSet):
    start_created_time = django_filters.DateFilter(field_name='created_time', lookup_expr='gte', label='开始创建')
    end_created_time = django_filters.DateFilter(field_name='created_time', lookup_expr='lte', label='结束创建')
    category = django_filters.NumberFilter(field_name='category')
    post_type = django_filters.NumberFilter(field_name='post_type')


class AllPostFilter(FilterSet):
    """首页过滤器"""
    category = django_filters.NumberFilter(required=True, field_name='category',
                                           method='filter_category', label='类别')

    def __init__(self, *args, **kwargs):
        super(FilterSet,self).__init__(*args, **kwargs)
        if self.request.parser_context['view'].action == 'retrieve':
            del self.filters['category']

    def filter_category(self, qs, name, value):
        qs = qs.defer('html_content', 'content')
        if value == 0:
            return qs.order_by('like_num')
        else:
            c = Category.objects.filter(id=value).first()
            if not c:
                c_range = []
            else:
                c_range = c.get_descendants(include_self=True).values_list('id', flat=True)
            return qs.filter(category__in=c_range)


class AuthorPostFilter(FilterSet):
    author = django_filters.NumberFilter(required=True, field_name='author',
                                        method='filter_author', label='作者')

    def filter_author(self, qs, name, value):
        return qs.filter(author=value).order_by('post_num')


class CategoryPostFilter(FilterSet):
    category = django_filters.NumberFilter(required=True, field_name='category',
                                           method='filter_category', label='类别')

    def filter_category(self, qs, name, value):
        return qs.filter(category=value).order_by('post_num')
