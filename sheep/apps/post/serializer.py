# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/3 18:51
from typing import Any

from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from apps.post.models import Category, Post, PostReply
from utils.extra_fields import CurrentUserIdDefault, SerializerMethodAndWriteField, RangeField
from sheep.constant import RET, error_map


User = get_user_model()


class PostCategorySerializer(serializers.ModelSerializer):
    """帖子无限级分类"""
    author_id = serializers.HiddenField(default=CurrentUserIdDefault())
    child = serializers.ReadOnlyField(label='全部子节点')
    name = serializers.CharField(validators=[
        UniqueValidator(
            queryset=Category.objects.all(),
            message={'code': RET.PARAMERR, 'msg':'分类名称已存在!'}
        )
    ])

    class Meta:
        model = Category
        fields = ["id", "name", "parent_id", "level", "desc", 'author_id', 'image', 'child', 'parent']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """帖子序列化器"""
    id = serializers.ReadOnlyField(label='帖子id')
    author_id = serializers.HiddenField(default=CurrentUserIdDefault(), label='创建人')
    post_num = serializers.ReadOnlyField(label='评论数量')
    read_num = serializers.ReadOnlyField(label='浏览数量')
    like_num = serializers.ReadOnlyField(label='收藏数量')
    praise_num = serializers.ReadOnlyField(label='点赞数量')
    is_active = serializers.ReadOnlyField(label='帖子状态')
    name = serializers.CharField(validators=[
        UniqueValidator(
            queryset=Post.objects.all(),
            message={'code':RET.PARAMERR, 'msg':'帖子名称已存在!'}
        )
    ])

    image = serializers.CharField(validators=[
        URLValidator(message='图片地址不正确!')
        ], label='封面', required=False, allow_null=True)
    category = SerializerMethodAndWriteField(label='帖子分类')
    content_type = RangeField(iterable=list(dict(Post.content_type_choices)),
                        label='文章类型',
                        required=True,
                        error_messages='文章类型传递错误!',
                        data_type=int
                        )

    def validate_category(self, category):
        if not category:
            raise serializers.ValidationError({'code': RET.PARAMERR,'msg': '类别必须选择'})
        c = category.pop()
        return c

    def get_category(self, category_id):
        obj = Category.objects.filter(id=category_id).first()
        return obj.get_ancestors(include_self=True).values_list('id', flat=True)

    author_info = serializers.SerializerMethodField(label='创建人信息')
    is_like = serializers.SerializerMethodField(label='是否收藏')
    is_praise = serializers.SerializerMethodField(label='是否点赞')

    def get_is_like(self, obj):
        from apps.operate.models import Collect
        return Collect.select_is_like(self.context['request'].user.id,
                                      1, obj.id)

    def get_is_praise(self, obj):
        from apps.operate.models import Praise
        return Praise.select_is_praise(self.context['request'].user.id,
                                       1, obj.id)

    def get_author_info(self, obj):
        """帖子创建人信息"""
        user = User.objects.filter(id=obj.author_id).values('id', 'username').first()
        if user:
            return dict(user)

    class Meta:
        model = Post
        exclude = ("content",)
        extra_kwargs = {
            'url': {'view_name': 'v1:web:all_post-detail', 'lookup_field': 'pk'},
        }
    ud_url = serializers.HyperlinkedIdentityField(view_name='v1:web:user_post-detail', lookup_field='pk')


class RetrievePostSerializer(PostSerializer):
    """retrieve方法的帖子序列化器"""

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            'url': {'view_name': 'v1:web:all_post-detail', 'lookup_field': 'pk'},
        }


class UserPostReplySerializer(serializers.ModelSerializer):
    """个人中心帖子回复序列化器"""
    praise_num = serializers.ReadOnlyField(label='点赞数量')
    is_active = serializers.ReadOnlyField(label='状态')

    post_id = serializers.IntegerField(label='回复帖子id')
    replier_id = serializers.ReadOnlyField(label='回复用户id')

    replier_info = serializers.SerializerMethodField(label='回复用户信息')
    type = serializers.SerializerMethodField(label='回复帖子/回复用户')
    post_info = serializers.SerializerMethodField(label='帖子信息')
    is_del = serializers.SerializerMethodField(label='是否可删除')

    def get_is_del(self, obj):
        """
        用户是否可以删除该回复,
        创建人是该用户&回复并没有子回复
        """
        return obj.is_del(self.context['request'].user.id)

    def get_type(self, obj):
        """
        获取回复的类型
        :return: 1-->回复帖子   2-->回复用户
        """
        return 1 if not obj.parent else 2

    def get_replier_info(self, obj):
        """
        返回回复人信息
        :param obj:
        :return:
        """
        if obj.replier_id:
            return User.get_simple_user_info(obj.replier_id)

    def get_post_info(self, obj):
        """
        返回帖子相关信息
        :param obj:
        :return:
        """
        return Post.get_simple_post_info(obj.post_id)

    class Meta:
        model = PostReply
        exclude = ("lft", "rght")


class PostReplySerializer(serializers.ModelSerializer):
    """帖子内回复序列化器"""
    praise_num = serializers.ReadOnlyField(label='点赞数量')
    is_active = serializers.ReadOnlyField(label='状态')
    replier_id = serializers.ReadOnlyField(label='回复用户id')
    author_id = serializers.HiddenField(default=CurrentUserIdDefault(), label='创建人')
    post_id = serializers.IntegerField(label='回复帖子id')

    def validate_post_id(self, post_id):
        post = Post.objects.filter(id=post_id).first()
        if post is None:
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': f'{post_id}回复帖子不存在!'})
        if not post.not_reply:
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': f'帖子{post.name},不允许回复!'})
        return post_id

    def validate(self, attr):
        parent = attr.get('parent')
        if parent:
            attr['replier_id'] = parent.author_id
        return attr

    replier_info = serializers.SerializerMethodField(label='回复用户信息')
    type = serializers.SerializerMethodField(label='回复帖子/回复用户')
    author_info = serializers.SerializerMethodField(label='创建人信息')
    is_del = serializers.SerializerMethodField(label='是否可删除')
    child_num = serializers.SerializerMethodField(label='子评论数量')

    def get_author_info(self, obj):
        """回复创建人信息"""
        user = User.get_simple_user_info(obj.author_id)
        if user:
            return user

    def get_replier_info(self, obj):
        """
        返回回复人信息
        :param obj:
        :return:
        """
        if obj.replier_id:
            return User.get_simple_user_info(obj.replier_id)

    def get_type(self, obj):
        """
        获取回复的类型
        :return: 1-->回复帖子   2-->回复用户
        """
        return 1 if not obj.parent else 2

    def get_is_del(self, obj):
        """
        用户是否可以删除该回复,
        创建人是该用户&回复并没有子回复
        """
        return obj.is_del(self.context['request'].user.id)

    def get_child_num(self, obj):
        """返回回复的子回复数量"""
        return obj.get_descendant_count()

    class Meta:
        model = PostReply
        exclude = ("lft", "rght")


class RetrievePostReplySerializer(PostReplySerializer):
    """帖子回复详情序列化器"""
    child = serializers.SerializerMethodField(label='用户子回复')

    def get_child(self, obj):
        """获取所有的子回复"""
        return PostReplySerializer(obj.get_descendants(), many=True, context=self.context).data

    class Meta:
        model = PostReply
        fields = ('id', 'author_id', 'child')