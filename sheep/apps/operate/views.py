from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from apps.operate.filters import CollectCategoryFilter, CollectFilter, PraiseFilter
from apps.user.serializer import ListCreateUserSerializer
from utils.mixins import CreateModelMixin
from utils.pagination import LimitOffsetPagination
from utils.viewsets import ModelViewSet, ReadOnlyModelViewSet
from utils.util import sort_queryset
from apps.operate.models import CollectCategory, Collect, TYPE_SERIALIZER_MAPPING, Praise, Focus
from apps.operate.serializer import CollectCategorySerializer, CreateCollectSerializer, CreateFocusSerializer


User = get_user_model()


class UserCollectCategoryViewSet(ModelViewSet):
    """用户收藏类别视图"""
    serializer_class = CollectCategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CollectCategoryFilter
    queryset = CollectCategory.objects.all()

    def get_queryset(self):
        # 当用户请求不是get时候,只能对用户自己的资源进行操作
        if self.request.method != 'GET':
            self.request.GET._mutable = True
            self.request.query_params['user_id'] = self.request.user.id
            self.request.GET._mutable = False
        return self.queryset

    def get_permissions(self):
        if self.action in {'list', 'retrieve'}:
            return ()
        return (i() for i in api_settings.DEFAULT_PERMISSION_CLASSES)


class CollectCategoryViewSet(ReadOnlyModelViewSet):
    """所有用户收藏类别视图"""
    serializer_class = CollectCategorySerializer
    lookup_field = 'user_id'
    queryset = CollectCategory.objects.filter(is_show=True)
    permission_classes = ()


class CollectViewSet(CreateModelMixin,
                     ListModelMixin,
                     GenericViewSet):
    """用户个人收藏的帖子"""
    queryset = Collect.objects.all()
    r_serializer_class = None
    c_serializer_class = CreateCollectSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    pagination_class = LimitOffsetPagination
    filterset_class = CollectFilter
    search_fields = ('name',)

    # 资源类型和serializer的映射
    TYPE_SERIALIZER = TYPE_SERIALIZER_MAPPING

    @property
    def type(self):
        """request的get参数type的值"""
        if not hasattr(self, '_type'):
            self._type = int(self.request.query_params.get('type'))
        return self._type

    def get_serializer_class(self):
        if self.action == 'create':
            return self.c_serializer_class
        return self.TYPE_SERIALIZER[self.type]

    def filter_queryset(self, queryset: QuerySet):
        queryset = super().filter_queryset(queryset)
        return Collect.TYPE_MODEL[self.type].objects.filter(id__in=queryset.values_list('resource_id', flat=True)).all()

    @transaction.atomic()
    def perform_create(self, serializer):
        instance = serializer.save()
        # 增加或减少对应资源的收藏数
        Collect.add_or_del_like_num(instance)


class PraiseViewSet(CreateModelMixin,
                     ListModelMixin,
                     GenericViewSet):
    """用户点赞视图"""
    r_serializer_class = None
    c_serializer_class = CreateCollectSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filterset_class = PraiseFilter

    # 资源类型和serializer的映射
    TYPE_SERIALIZER = TYPE_SERIALIZER_MAPPING

    @property
    def type(self):
        """request的get参数type的值"""
        if not hasattr(self, '_type'):
            self._type = int(self.request.query_params.get('type'))
        return self._type

    def get_queryset(self):
        return Praise.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return self.c_serializer_class
        return self.TYPE_SERIALIZER[self.type]

    def filter_queryset(self, queryset: QuerySet):
        queryset = super().filter_queryset(queryset)
        return Praise.TYPE_MODEL[self.type].objects.filter(id=queryset.values_list('resource_id', flat=True)).all()

    @transaction.atomic()
    def perform_create(self, serializer):
        instance = serializer.save()
        # 增加或减少对应资源的点赞数
        Praise.add_or_del_praise_num(instance)


class FocusViewSet(ListModelMixin,
                   CreateModelMixin,
                   GenericViewSet):
    """关注视图"""
    c_serializer_class = CreateFocusSerializer
    r_serializer_class = ListCreateUserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', self.request.user.id)
        type = int(self.request.query_params.get('type', 1))
        # type为1时, 查看我关注的人
        if type == 1:
            focus_ids = Focus.objects.filter(user_id=user_id).values_list('focus_id', flat=True)
        # type为其它值时, 查看关注我的人
        else:
            focus_ids = Focus.objects.filter(focus_id=user_id).values_list('user_id', flat=True)
        return sort_queryset(User, focus_ids)

    def get_serializer_class(self):
        if self.action == 'create':
            return self.c_serializer_class
        return self.r_serializer_class

    def get_permissions(self):
        if self.action != 'create':
            return []
        return super().get_permissions()
