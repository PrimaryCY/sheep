import datetime

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from apps.operate.tasks import after_collect, after_delete_user_category
from apps.operate.filters import PraiseFilter
from apps.post.filters import PostFilter
from apps.post.models import Post
from apps.post.serializer import PostSerializer
from apps.user.permission import IsLoginUser
from sheep.constant import RET, error_map
from utils.viewsets import ExtensionViewMixin
from utils.django_util.util import field_sort_queryset, raw_sort_queryset
from utils.mixins import CreateModelMixin
from utils.pagination import LimitOffsetPagination
from utils.viewsets import ModelViewSet, ReadOnlyModelViewSet
from apps.operate.models import CollectCategory, Praise, Focus, \
    CollectRedisModel, BrowsingHistoryRedisMode
from apps.operate.serializer import CollectCategorySerializer, CreateCollectSerializer, \
    CreateFocusSerializer, CollectPostSerializer, ListPraiseSerializer, CreatePraiseSerializer, \
    BrowsingHistorySerializer, ListFocusSerializer

User = get_user_model()


class UserCollectCategoryViewSet(ModelViewSet):
    """用户收藏类别视图"""
    serializer_class = CollectCategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['resource_id'] = self.request.query_params.get('resource_id', None)
        context['user_id'] = self.request.user.id
        return context

    def get_queryset(self):
        return CollectCategory.objects.filter(user_id=self.request.user.id).all()

    def perform_destroy(self, instance):
        CollectCategory.objects.filter(id=instance.id).update(is_active=False)
        after_delete_user_category.delay(instance.user_id, instance.id)


class CollectCategoryViewSet(ReadOnlyModelViewSet):
    """所有用户收藏类别视图"""
    serializer_class = CollectCategorySerializer
    lookup_field = 'user_id'
    queryset = CollectCategory.objects.filter(is_show=True)
    permission_classes = ()


class CollectViewSet(CreateModelMixin,
                     ExtensionViewMixin,
                     ListModelMixin,
                     GenericViewSet):
    """用户个人收藏的帖子"""
    serializer_class = {
        'create': CreateCollectSerializer,
        'list': CollectPostSerializer
    }
    c_serializer_class = CreateCollectSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    pagination_class = LimitOffsetPagination
    filter_class = PostFilter
    search_fields = ('name',)

    def get_queryset(self):
        category_id = self.request.query_params.get('collect_id')
        if not category_id:
            raise ValidationError({'success': False,
                                   'code': RET.PARAMERR,
                                   'msg': error_map[RET.PARAMERR]})
        self.collect_dict = CollectRedisModel(self.request.user.id, category_id).get_all(self.request)
        collect_resource_ids = self.collect_dict.keys()
        return field_sort_queryset(Post.raw_objects, collect_resource_ids)

    def paginate_queryset(self, queryset):
        queryset_list = super().paginate_queryset(queryset)
        for i in queryset_list:
            date_array = datetime.datetime.fromtimestamp(self.collect_dict.get(i.id))
            i.created_like_time = date_array.strftime("%Y-%m-%d %H:%M")
        return queryset_list

    @transaction.atomic()
    def perform_create(self, serializer):
        attr = serializer.save()
        after_collect.delay(**attr)


class PraiseViewSet(CreateModelMixin,
                    ExtensionViewMixin,
                    ListModelMixin,
                    GenericViewSet):
    """用户点赞视图"""
    serializer_class = {
        'list': ListPraiseSerializer,
        'create': CreatePraiseSerializer
    }
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filter_class = PraiseFilter
    permission_classes = ()

    def get_queryset(self):
        # 仅支持用户看到自己点赞的文章
        # 暂不支持查看点赞的评论
        return Praise.objects.filter(t=1, user_id=self.request.user.id)

    def paginate_queryset(self, queryset):
        queryset_list = super().paginate_queryset(queryset)
        post_ids = {i.resource_id: (i.update_time, i.praise_or_trample) for i in queryset_list}
        real_post = raw_sort_queryset(Post.raw_objects, post_ids.keys())
        for i in real_post:
            i.update_praise_time, i.praise_or_trample = post_ids.get(i.id)
        return real_post


class BrowsingHistoryViewSet(ListModelMixin,
                             GenericViewSet):
    """用户浏览记录视图"""
    serializer_class = BrowsingHistorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsLoginUser,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = PostFilter
    search_fields = ('name',)

    def get_queryset(self):
        self.history_dict = BrowsingHistoryRedisMode(self.request.user.id).get_all(self.request)
        collect_resource_ids = self.history_dict.keys()
        return field_sort_queryset(Post.raw_objects, collect_resource_ids)

    def paginate_queryset(self, queryset):
        queryset_list = super().paginate_queryset(queryset)
        for i in queryset_list:
            date_array = datetime.datetime.fromtimestamp(self.history_dict.get(i.id))
            i.created_history_time = date_array.strftime("%Y-%m-%d %H:%M")
        return queryset_list


class FocusViewSet(ExtensionViewMixin,
                   ListModelMixin,
                   CreateModelMixin,
                   GenericViewSet):
    """关注视图"""
    serializer_class = {
        'create': CreateFocusSerializer,
        'list': ListFocusSerializer
    }
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = None

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', self.request.user.id)
        type = int(self.request.query_params.get('type', 1))
        # type为1时, 查看我关注的人
        if type == 1:
            focus_ids = Focus.objects.filter(user_id=user_id).values_list('focus_id', flat=True)
        # type为其它值时, 查看关注我的人
        else:
            focus_ids = Focus.objects.filter(focus_id=user_id).values_list('user_id', flat=True)
        return raw_sort_queryset(User.raw_objects.only(*ListFocusSerializer.Meta.fields), focus_ids)
