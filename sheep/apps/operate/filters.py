# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/20 15:24
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from apps.operate.models import CollectCategory, Collect, Praise, Focus
from utils.util import sort_queryset


User = get_user_model()

#
# class CollectCategoryFilter(filters.FilterSet):
#     # user_id = filters.NumberFilter(method='filter_user_id', label='用户id', required=True)
#     #
#     # def filter_user_id(self, queryset, name, value):
#     #     # 当筛选用户是自己时, 展示自己的所有收藏分类
#     #     if value == self.request.user.id:
#     #         return queryset.filter(user_id=value).all()
#     #     # 当用户在看他人的收藏类别时, 展示他人想展示的收藏分类
#     #     else:
#     #         return queryset.filter(user_id=value, is_show=True).all()
#
#     class Meta:
#         model = CollectCategory
#         fields = ('',)


class CollectFilter(filters.FilterSet):
    category_id = filters.NumberFilter(label='收藏分类id', required=True)
    type = filters.ChoiceFilter(choices=Collect.TYPE_CHOICES, label='收藏资源分类', required=True)

    class Meta:
        model = Collect
        fields = ('category_id', 'type')


class PraiseFilter(filters.FilterSet):
    type = filters.ChoiceFilter(choices=Collect.TYPE_CHOICES, label='点赞资源分类', required=True)

    class Meta:
        model = Praise
        fields = ('type', )


class FocusFilter(filters.FilterSet):
    FOCUSTYPE_CHOICES = (
        (1, '我关注的人'),
        (2, '关注我的人')
    )
    type = filters.ChoiceFilter(choices=FOCUSTYPE_CHOICES, label='关注', required=True)

    def filter_user_id(self, queryset, name, value):
        user_id = self.request.query_params.get('user_id', self.request.user.id)
        # type为1时, 查看我关注的人
        if value == 1:
            focus_ids = queryset.filter(user_id=user_id).values_list('focus_id', flat=True)
        # type为其它值时, 查看关注我的人
        else:
            focus_ids = queryset.filter(focus_id=user_id).values_list('user_id', flat=True)
        return sort_queryset(User, focus_ids)

    class Meta:
        model = Focus
        fields = ('type',)