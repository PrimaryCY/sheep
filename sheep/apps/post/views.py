from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework_extensions.utils import default_list_cache_key_func

from apps.post.models import Category, Post, PostReply
from apps.post.filters import PostFilter
from utils.viewsets import ModelViewSet, CreateModelMixin, DestroyModelMixin
from utils.pagination import LimitOffsetPagination
from utils.drf_extensions.decorators import only_data_cache_response
from apps.post.serializer import PostCategorySerializer, UserPostSerializer, PostReplySerializer, RetrievePostReplySerializer, UpdateRetrieveUserPostSerializer
from apps.user.permission import IsAdminUser, IsLoginUser


class PostCategoryViewSet(ModelViewSet):
    """帖子类别视图"""
    serializer_class = PostCategorySerializer
    queryset = Category.objects.all()
    list_queryset = Category.objects.filter(level=0)
    list_permission_classes = ()
    other_permission_classes = (IsAdminUser,)

    def get_permissions(self):
        # 只有管理员能对分类进行增删改
        if self.action not in {'list', 'retrieve'}:
            return [i() for i in self.other_permission_classes]
        return [i() for i in self.list_permission_classes]

    def get_queryset(self):
        if self.action == 'list':
            # list接口只展示根节点的分类
            return self.list_queryset
        return self.queryset


class UserPostViewSet(ModelViewSet):
    """个人帖子视图"""
    serializer_class = UserPostSerializer
    retrieve_serializer_class = UpdateRetrieveUserPostSerializer
    permission_classes = (IsLoginUser,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = PostFilter
    search_fields = ('name',)
    ordering_fields = "__all__"

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        return self.retrieve_serializer_class

    def get_queryset(self):
        if self.action == 'list':
            return Post.raw_objects.filter(author_id=self.request.user.id).all()
        return Post.objects.filter(author_id=self.request.user.id).all()

    def retrieve(self, request, *args, **kwargs):
        """重写retrieve方法  增加阅读数"""
        instance = self.get_object()
        instance.add_read_num(instance.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserReplyViewSet(ReadOnlyModelViewSet,
                       DestroyModelMixin):
    """个人帖子回复视图"""
    serializer_class = PostReplySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (OrderingFilter,)
    ordering_fields = ('create_time', 'praise_num')

    def get_queryset(self):
        return PostReply.objects.filter(author_id=self.request.user.id, post_id__isnull=False).all()

    @transaction.atomic()
    def perform_destroy(self, instance):
        if not (instance.author_id == self.request.user.id and
                instance.get_descendant_count() <= 0):
            raise serializers.ValidationError({'code': ...})
        super().perform_destroy(instance)
        # 减少帖子回复数量
        Post.del_post_num(instance.post_id)


class PostReplyViewSet(ReadOnlyModelViewSet,
                       CreateModelMixin):
    """帖子回复视图"""
    serializer_class = PostReplySerializer
    retrieve_serialize_class = RetrievePostReplySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (OrderingFilter,)
    ordering_fields = ('create_time', 'praise_num')
    permission_classes = ()

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        return PostReply.objects.filter(post_id=post_id, parent__isnull=True)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.retrieve_serialize_class
        return self.serializer_class

    @transaction.atomic()
    def perform_create(self, serializer):
        instance = serializer.save()
        # 增加帖子回复数量
        Post.add_post_num(instance.post_id)
