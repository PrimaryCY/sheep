# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/6/29 23:23
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.post.models import Post

User = get_user_model()


class BannerSerializer(serializers.Serializer):
    """轮播图序列化器"""
    id = serializers.IntegerField()
    image = serializers.URLField(label='封面链接')
    name = serializers.CharField(label='标题')


class HotSerializer(serializers.Serializer):
    """热门序列化器"""
    id = serializers.IntegerField()
    name = serializers.CharField(label='标题')
    post_type = serializers.IntegerField(label='文章类别')
    read_num = serializers.IntegerField(label='阅读数量')
    image = serializers.URLField(label='封面')


