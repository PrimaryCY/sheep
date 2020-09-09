# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/19 13:36
from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import serializers

from apps.operate.models import CollectCategory, Collect, Praise, Focus, CollectRedisModel
from apps.post.models import Post
from apps.post.serializer import PostSerializer
from sheep.constant import RET
from utils.extra_fields import CurrentUserIdDefault, RangeField


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
    image = serializers.URLField(label='封面图片', required=False, allow_blank=True)
    desc = serializers.CharField(label='描述', allow_blank=True, required=False)
    total = serializers.ReadOnlyField(label='文章总和')
    is_like = serializers.SerializerMethodField(label='资源是否在此收藏集中')
    created_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d', label='创建日期')

    # redis版本
    def get_is_like(self, obj):
        if self.context.get('resource_id') :
            model = CollectRedisModel(self.context['user_id'], obj.id)
            return model.get_is_like(self.context['resource_id'])
        return False

    class Meta:
        model = CollectCategory
        fields = "__all__"


class CreateCollectSerializer(serializers.Serializer):
    """用户收藏序列化器"""
    user_id = serializers.HiddenField(default=CurrentUserIdDefault(), label='用户id')
    category_id = serializers.IntegerField(label='收藏类别id')
    resource_id = serializers.IntegerField(label='资源id')

    # 去除校验,增加速度
    # def validate_category_id(self, category_id):
    #     res = CollectCategory.objects.filter(id=category_id, user_id=self.context['request'].user.id).only('id')
    #     if not res:
    #         raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '用户不存在该分类!'})
    #     return category_id
    #
    # def validate(self, attr):
    #     type = attr.get('type')
    #     resource_id = attr.get('resource_id')
    #     resource = Collect.TYPE_MODEL[type].objects.filter(id=resource_id).only('id').first()
    #     if not resource:
    #         raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '不存在该资源!'})
    #     return attr

    def create(self, attr: dict):
        user_id = self.context['request'].user.id
        resource_id = attr.get('resource_id')
        category_id = attr.get('category_id')
        model = CollectRedisModel(user_id, category_id)
        is_active = model.create_or_delete(resource_id)
        attr['is_active'] = is_active
        self._data = {'success': True, 'code': RET.OK, 'data': '💕收藏成功!' if is_active else '💔取消收藏...'}
        return attr


class CreatePraiseSerializer(serializers.Serializer):
    """用户点赞序列化器"""
    resource_id = serializers.IntegerField(label='资源id')
    praise_or_trample = serializers.IntegerField(label='点赞或是踩')
    t = RangeField(iterable=list(Praise.PRAISE_TYPE_CHOICE), data_type=int)

    def validate(self, attr):
        resource_id = attr.get('resource_id')
        resource = Post.objects.filter(id=resource_id).only('id').exists()
        if not resource:
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '不存在该资源!'})
        return attr

    def create(self, validated_data: dict):
        user_id = self.context['request'].user.id
        resource_id = validated_data.get('resource_id')
        praise_or_trample = validated_data.get('praise_or_trample')
        t = validated_data.get('t')
        return_num = Praise.add_or_del_praise_num(user_id=user_id,
                                                  resource_id=resource_id,
                                                  praise_or_trample=praise_or_trample,
                                                  t=t)

        temp = {
            1: '💕点赞成功！',
            0: '💔取消成功...',
            -1: '👎的漂亮！'
        }
        self._data = {
            "success": True,
            "code": RET.OK,
            "data": {
                'msg': temp.get(praise_or_trample),
                'return_num': return_num
            }
        }
        return validated_data


class ListPraiseSerializer(PostSerializer):
    """点赞/踩列表页序列化器"""
    update_praise_time = serializers.DateTimeField(read_only=True, label='点赞/踩时间')
    praise_or_trample = serializers.IntegerField(read_only=True, label='点赞状态')
    newest_user_id = None

    class Meta:
        model = Post
        exclude = ("content", "html_content")


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


class CollectPostSerializer(PostSerializer):
    """收藏列表页序列化器"""
    created_like_time = serializers.DateTimeField(read_only=True, label='收藏时间')
    newest_user_id = None

    class Meta:
        model = Post
        exclude = ("content", "html_content")