# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/6/29 23:23
from rest_framework import serializers

from apps.post.models import Post


class IndexSerializer(serializers.Serializer):
    """首页序列化器"""
    banner = serializers.SerializerMethodField(label='轮播图')

    def get_banner(self, obj):
        return Post.get_banner()
