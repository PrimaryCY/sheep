# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/3 18:51
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import serializers
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
        fields = ["id", "name", "parent_id", "level", "desc", 'author_id', 'child', 'parent']


# class PostSerializer(serializers.HyperlinkedModelSerializer):
class UserPostSerializer(serializers.ModelSerializer):
    """帖子序列化器"""
    id = serializers.ReadOnlyField(label='帖子id')
    author_id = serializers.HiddenField(default=CurrentUserIdDefault(), label='创建人')
    post_num = serializers.ReadOnlyField(label='评论数量')
    read_num = serializers.ReadOnlyField(label='浏览数量')
    like_num = serializers.ReadOnlyField(label='收藏数量')
    praise_num = serializers.ReadOnlyField(label='点赞数量')
    status = serializers.ReadOnlyField(label='帖子状态')
    name = serializers.CharField(validators=[
        UniqueValidator(
            queryset=Post.objects.all(),
            message={'code':RET.PARAMERR, 'msg':'帖子名称已存在!'}
        )
    ])

    category = serializers.ListField(label='帖子分类', write_only=True)
    content_type = RangeField(iterable=list(dict(Post.content_type_choices)),
                        label='文章书写类型',
                        required=True,
                        error_messages='文章书写类型传递错误!',
                        data_type=int
                        )

    post_type = RangeField(iterable=list(dict(Post.post_type_choices)),
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

    class Meta:
        model = Post
        exclude = ("content", "html_content")
        # extra_kwargs = {
        #     'url': {'view_name': 'v1:web:post-detail', 'lookup_field': 'pk'},
        # }
    # ud_url = serializers.HyperlinkedIdentityField(view_name='v1:web:user_post-detail', lookup_field='pk')


class UpdateRetrieveUserPostSerializer(UserPostSerializer):
    """个人文章查改方法的帖子序列化器"""
    desc = serializers.ReadOnlyField(label='帖子简介')
    html_content = serializers.CharField(write_only=True, label='html内容')
    content = serializers.CharField(write_only=True, label='文字内容', error_messages={
        'null': '文章内容必须要输入一些内容!',
        'blank': '文章内容必须要输入一些内容!',
    })
    parse_content = serializers.SerializerMethodField(label='帖子编辑内容')
    category_list = serializers.SerializerMethodField(label='类别列表')

    def get_category_list(self, obj):
        category = Category.objects.filter(id=obj.category).first()
        return category.get_ancestors(include_self=True).values_list('id', flat=True)

    def get_parse_content(self, obj):
        return obj.content if obj.content_type == 2 else obj.html_content

    def validate(self, attrs):
        content = attrs.get('content')
        if content:
            # 帖子简介
            attrs['desc'] = content[:230]
        return attrs

    class Meta:
        model = Post
        exclude = ('newest_user_id',)
        extra_kwargs = {
            'url': {'view_name': 'v1:web:post-detail', 'lookup_field': 'pk'},
        }


class UserPostReplySerializer(serializers.ModelSerializer):
    """个人中心帖子回复序列化器"""
    praise_num = serializers.ReadOnlyField(label='点赞数量')
    status = serializers.ReadOnlyField(label='状态')

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
    status = serializers.ReadOnlyField(label='状态')
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


class PostSerializer(serializers.ModelSerializer):
    """帖子序列化器"""
    id = serializers.ReadOnlyField(label='帖子id')
    post_num = serializers.ReadOnlyField(label='评论数量')
    read_num = serializers.ReadOnlyField(label='浏览数量')
    like_num = serializers.ReadOnlyField(label='收藏数量')
    praise_num = serializers.ReadOnlyField(label='点赞数量')
    status = serializers.ReadOnlyField(label='帖子状态')
    desc = serializers.ReadOnlyField(label='帖子简介')
    name = serializers.CharField(label='帖子标题')
    content_type = serializers.IntegerField(label='文章书写类型')
    post_type = serializers.IntegerField(label='文章类型')

    author_info = serializers.SerializerMethodField(label='创建人信息')
    newest_user_id = serializers.SerializerMethodField(label='最新回复人')

    def get_newest_user_id(self, post):
        u_id = post.newest_user_id
        if not u_id:
            return u_id
        return User.get_simple_user_info(u_id)

    def get_author_info(self, obj):
        """帖子创建人信息"""
        if obj.author_id == self.context['request'].user.id:
            user = self.context['request'].user
            return dict(id=user.id,
                        portrait=user.portrait,
                        username=user.username)
        user = User.get_simple_user_info(obj.author_id)
        return user

    class Meta:
        model = Post
        exclude = ("content", "html_content")


class RetrievePostSerializer(PostSerializer):
    """retrieve方法的帖子序列化器"""
    author_info = serializers.SerializerMethodField(label='创建人信息')
    category = serializers.SerializerMethodField(label='分类')
    category_id = serializers.IntegerField(label='分类id', source='category')

    is_like = serializers.SerializerMethodField(label='是否收藏')
    is_praise = serializers.SerializerMethodField(label='是否点赞')

    def get_is_like(self, obj):
        from apps.operate.models import CollectRedisModel
        user = self.context['request'].user
        return CollectRedisModel.get_user_is_like(user, obj.id)

    def get_is_praise(self, obj):
        from apps.operate.models import Praise
        return Praise.select_is_praise(self.context['request'].user.id,
                                       obj.id, 1)

    def get_author_info(self, obj):
        """帖子创建人信息"""
        if obj.author_id == self.context['request'].user.id:
            res = User.get_post_retrieve_author_info(self.context['request'].user)
        else:
            res = User.get_post_retrieve_author_info(obj.author_id)
        return res

    def get_category(self, obj):
        c = Category.objects.filter(id=obj.category).only('name').first()
        if not c:
            return '不告诉你!'
        return c.name

    class Meta:
        model = Post
        exclude = ('content',)
        extra_kwargs = {
            'url': {'view_name': 'v1:web:post-detail', 'lookup_field': 'pk'},
        }


class CorrelationCategorySerializer(serializers.ModelSerializer):
    article_total = serializers.SerializerMethodField(label='该分类下的文章总数')

    def get_article_total(self, obj):
        return Post.objects.filter(category=obj.id).only('id').count()

    class Meta:
        model = Category
        fields = ["id", "name", "parent_id", "level", "article_total"]
