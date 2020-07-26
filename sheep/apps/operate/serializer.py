# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/19 13:36
from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import serializers

from apps.operate.models import CollectCategory, Collect, Praise, Focus
from apps.post.models import Post
from sheep.constant import RET
from utils.extra_fields import CurrentUserIdDefault


User = get_user_model()


class CollectCategorySerializer(serializers.ModelSerializer):
    """收藏分类视图"""
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='v1:web:user_collect-detail',
    #     lookup_field='pk'
    # )
    user_id = serializers.HiddenField(default=CurrentUserIdDefault(), label='用户')
    is_active = serializers.ReadOnlyField(label='状态')
    is_show = serializers.BooleanField(label='是否可见', required=False)
    image = serializers.URLField(label='封面图片', required=False)
    desc = serializers.CharField(label='描述', default='')
    total = serializers.SerializerMethodField(label='文章总和')

    def get_total(self, obj):
        return Collect.objects.filter(category_id=obj.id).only('id').count()

    class Meta:
        model = CollectCategory
        fields = "__all__"


class CreateCollectSerializer(serializers.Serializer):
    """用户收藏序列化器"""
    user_id = serializers.HiddenField(default=CurrentUserIdDefault(), label='用户id')
    is_active = serializers.ReadOnlyField(label='状态')
    category_id = serializers.IntegerField(label='收藏类别id')
    resource_id = serializers.IntegerField(label='资源id')
    type = serializers.ChoiceField(choices=Collect.TYPE_CHOICES, label='收藏类型')
    created_time = serializers.DateTimeField(read_only=True, label='收藏时间')

    def validate_category_id(self, category_id):
        res = CollectCategory.objects.filter(id=category_id, user_id=self.context['request'].user.id).only('id')
        if not res:
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '用户不存在该分类!'})
        return category_id

    def validate(self, attr):
        type = attr.get('type')
        resource_id = attr.get('resource_id')
        resource = Collect.TYPE_MODEL[type].objects.filter(id=resource_id).only('id').first()
        if not resource:
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '不存在该资源!'})
        return attr

    def create(self, validated_data: dict):
        type = validated_data.get('type')
        resource_id = validated_data.get('resource_id')
        category_id = validated_data.get('category_id')
        user_id = validated_data.get('user_id')
        obj, created = Collect.raw_objects.get_or_create(resource_id=resource_id, category_id=category_id, type=type, user_id=user_id, defaults=validated_data)
        if not created:
            obj.is_active = not F('is_active')
            obj.save()
        return obj


class CreatePraiseSerializer(serializers.Serializer):
    """用户点赞序列化器"""
    is_active = serializers.ReadOnlyField(label='状态')
    resource_id = serializers.IntegerField(label='资源id')
    type = serializers.ChoiceField(choices=Collect.TYPE_CHOICES, label='点赞类型')
    created_time = serializers.DateTimeField(read_only=True, label='点赞时间')

    def validate(self, attr):
        type = attr.get('type')
        resource_id = attr.get('resource_id')
        resource = Praise.TYPE_MODEL[type].objects.filter(id=resource_id).only('id').first()
        if not resource:
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '不存在该资源!'})
        return attr

    def create(self, validated_data: dict):
        type = validated_data.get('type')
        resource_id = validated_data.get('resource_id')
        obj, created = Collect.raw_objects.get_or_create(resource_id=resource_id, type=type, defaults=validated_data)
        if not created:
            obj.is_active = not F('is_active')
            obj.save()
        return obj


class CreateFocusSerializer(serializers.Serializer):
    """用户关注序列化器"""
    is_active = serializers.ReadOnlyField(label='状态')
    user_id = serializers.HiddenField(default=CurrentUserIdDefault(), label='用户id')
    focus_id = serializers.IntegerField(label='关注用户id')
    created_time = serializers.DateTimeField(read_only=True, label='关注时间')

    def validate_focus_id(self, focus_id):
        if focus_id == self.context['request'].user.id:
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '用户不能关注自己!'})
        focus_user = User.objects.filter(id=focus_id).first()
        if not focus_user:
            raise serializers.ValidationError({"code": RET.PARAMERR, 'msg': '不存在该用户!'})
        return focus_id

    def create(self, validated_data: dict):
        user_id = validated_data.get('user_id')
        focus_id = validated_data.get('focus_id')
        obj, created = Focus.raw_objects.get_or_create(focus_id=focus_id, user_id=user_id, defaults=validated_data)
        if not created:
            obj.is_active = not F('is_active')
            obj.save()
        return obj
