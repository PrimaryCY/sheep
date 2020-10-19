from django.db import transaction
from django.db.models import Q
from django.db.transaction import on_commit
from django.forms import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework.settings import api_settings

from apps.operate.models import Praise
from apps.post.models import Category, Post, PostReply, User
from apps.post.tasks import after_retrieve_post, after_create_post_reply, after_delete_post_reply, after_list_reply
from apps.post.filters import PostFilter, AllPostFilter, AuthorPostFilter, CategoryPostFilter, CorrelationCategoryFilter
from sheep.constant import RET
from utils.drf_extensions.util import limit_offset_list_cache_key_func
from utils.viewsets import ModelViewSet, CreateModelMixin, DestroyModelMixin, GenericViewSet, ReadOnlyModelViewSet, \
    ExtensionViewMixin, SerializerContextViewMixin
from utils.pagination import LimitOffsetPagination
from utils.drf_extensions.decorators import only_data_cache_response
from apps.post.serializer import PostCategorySerializer, UserPostSerializer, CreateUserPostReplySerializer, \
    UpdateRetrieveUserPostSerializer, PostSerializer, RetrievePostSerializer, CorrelationCategorySerializer, \
    ListUserPostReplySerializer
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

    def perform_destroy(self, instance):
        instance.status = 1
        instance.save()


class UserReplyViewSet(SerializerContextViewMixin,
                       ReadOnlyModelViewSet,
                       CreateModelMixin,
                       DestroyModelMixin):
    """个人帖子回复视图"""
    serializer_class = {
        "list": ListUserPostReplySerializer,
        "create": CreateUserPostReplySerializer,
    }
    pagination_class = LimitOffsetPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('created_time', 'praise_num')
    filter_fields = ('is_read',)

    def get_serializer_context(self, qs, many):
        context = super().get_serializer_context()
        if self.action in {'retrieve', 'create', 'update', 'partial_update'}:
            return context

        context['author_info'] = User.bulk_get_simple_user_info([i.author_id for i in qs])
        context['post_info'] = Post.bulk_get_simple_post_info([i.post_id for i in qs])
        return context

    def get_permissions(self):
        if self.action == 'create':
            return ()
        return (temp() for temp in api_settings.DEFAULT_PERMISSION_CLASSES)

    def get_queryset(self):
        if self.action == 'destroy':
            pk = self.kwargs.get('pk')
            if PostReply.objects.filter(parent_id=pk,
                                        is_active=True,
                                        author_id=self.request.user.id).exists():
                raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '参数传递错误！'})
            return PostReply.objects.filter(author_id=self.request.user.id, is_active=True).all()
        elif self.action == 'list':
            # post_ids = Post.raw_objects.filter(author_id=self.request.user.id).values_list('id', flat=True)
            # return PostReply.objects.filter(
            #     Q(replier_id=self.request.user.id) | Q(Q(post_id__in=post_ids) & Q(parent_id__isnull=True)))
            return PostReply.objects.filter(replier_id=self.request.user.id)
        # return PostReply.objects.filter(author_id=self.request.user.id).all()

    def perform_create(self, serializer):
        instance = serializer.save()
        after_create_post_reply.delay(instance.post_id,
                                      instance.author_id)

    @transaction.atomic()
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        on_commit(lambda: after_delete_post_reply.delay(instance.post_id))


class PostReplyViewSet(GenericViewSet):
    """所有帖子回复视图"""
    pagination_class = LimitOffsetPagination
    filter_backends = (OrderingFilter,)
    ordering_fields = ('-created_time', 'praise_num')
    permission_classes = ()
    queryset = PostReply.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            post_id = int(request.query_params.get('post_id'))
        except:
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '参数传递错误'})

        qs = PostReply.objects.filter(post_id=post_id, parent__isnull=True).defer("lft", "rght")

        filter_qs = self.filter_queryset(qs)
        paginate_qs = self.paginate_queryset(filter_qs)

        users_info = User.get_simple_users_info([i.author_id for i in paginate_qs])

        celery_ids = []
        return_list = []
        for obj in paginate_qs:
            dic = model_to_dict(obj)
            dic['created_time'] = obj.created_time.strftime("%Y-%m-%d %H:%M:%S")
            dic['update_time'] = obj.update_time.strftime("%Y-%m-%d %H:%M:%S")
            dic['author_info'] = users_info.get(obj.author_id)
            dic['is_del'] = obj.is_del(request.user.id)
            dic['is_praise'] = Praise.select_is_praise(request.user.id,
                                                       obj.id, 2)
            dic['children'] = []
            children = obj.get_descendants().filter(is_active=True).defer("lft", "rght")
            child_users_info = User.get_simple_users_info([child.author_id for child in children])

            for child in children:
                child_dict = model_to_dict(child)
                child_dict['author_info'] = child_users_info.get(child.author_id)
                child_dict['is_del'] = child.is_del(request.user.id)
                child_dict['is_praise'] = Praise.select_is_praise(request.user.id,
                                                                  child.id, 2)
                child_dict['created_time'] = child.created_time.strftime("%Y-%m-%d %H:%M:%S")
                child_dict['update_time'] = child.update_time.strftime("%Y-%m-%d %H:%M:%S")
                dic['children'].append(child_dict)
                # 添加id celery任务修改已读未读状态
                celery_ids.append(child_dict['id'])

            return_list.append(dic)
            celery_ids.append(dic['id'])
        if not request.user.is_anonymity:
            after_list_reply.delay(request.user.id, celery_ids)
        return self.get_paginated_response(return_list)


class AllPostViewSet(ReadOnlyModelViewSet):
    """所有帖子视图"""
    serializer_class = {
        'list': PostSerializer,
        'retrieve': RetrievePostSerializer
    }
    permission_classes = ()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = AllPostFilter
    queryset = Post.objects.all()

    @only_data_cache_response(key_func=limit_offset_list_cache_key_func)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """重写retrieve方法  增加阅读数"""
        instance = self.get_object()
        user = self.request.user
        after_retrieve_post.delay(resource_id=instance.id,
                                  user_id=user.id,
                                  is_anonymity=user.is_anonymity)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AuthorPostViewSet(ListModelMixin,
                        GenericViewSet):
    """
    作者相关文章推荐
    """
    queryset = Post.objects
    permission_classes = ()
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filter_class = AuthorPostFilter
    serializer_class = PostSerializer

    @only_data_cache_response(key_func=limit_offset_list_cache_key_func)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CategoryPostViewSet(ListModelMixin,
                          GenericViewSet):
    """
    分类相关文章推荐
    """
    queryset = Post.objects
    permission_classes = ()
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filter_class = CategoryPostFilter
    serializer_class = PostSerializer

    @only_data_cache_response(key_func=limit_offset_list_cache_key_func)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CorrelationCategoryViewSet(ListModelMixin,
                                 GenericViewSet):
    """
    相关分类
    """
    queryset = Category.objects
    permission_classes = ()
    filter_backends = (DjangoFilterBackend,)
    filter_class = CorrelationCategoryFilter
    serializer_class = CorrelationCategorySerializer

    @only_data_cache_response(key_func=limit_offset_list_cache_key_func)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
