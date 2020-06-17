# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/6/2 20:37
import django_filters
from django.db import models
from django_filters import FilterSet

from apps.other.models import Feedback, UploadHistoryModel


class FeedbackFilter(FilterSet):
    start_created_time = django_filters.DateFilter(field_name='created_time', lookup_expr='gte', label='开始创建')
    end_created_time = django_filters.DateFilter(field_name='created_time', lookup_expr='lte', label='结束创建')
    category_id = django_filters.NumberFilter(field_name='category_id', label='反馈类别')
    author_id = django_filters.NumberFilter(field_name='author_id', label='创建人')
    has_reply = django_filters.BooleanFilter(method='filter_has_reply', label='只看有回复')

    def filter_has_reply(self, queryset, name, value):
        if value:
            return queryset.filter(reply_author_id__isnull=False)
        return queryset

    class Meta:
        model = Feedback
        fields = ('category_id', 'author_id', 'start_created_time', 'end_created_time', 'has_reply')


class UploadHistoryFilter(FilterSet):

    class Meta:
        model = UploadHistoryModel
        fields = ['user_id', 'url']
        filter_overrides = {
            models.FileField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }