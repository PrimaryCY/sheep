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

from apps.operate.filters import CollectFilter, PraiseFilter
from apps.operate.tasks import after_collect
from apps.post.models import Post
from apps.post.serializer import PostSerializer
from apps.user.serializer import ListCreateUserSerializer
from sheep.constant import RET, error_map
from utils.viewsets import ExtensionViewMixin
from utils.django_util.util import field_sort_queryset
from utils.mixins import CreateModelMixin
from utils.pagination import LimitOffsetPagination
from utils.viewsets import ModelViewSet, ReadOnlyModelViewSet
from apps.operate.models import CollectCategory, TYPE_SERIALIZER_MAPPING, Praise, Focus, \
    CollectRedisModel
from apps.operate.serializer import CollectCategorySerializer, CreateCollectSerializer, CreateFocusSerializer


User = get_user_model()


class UserCollectCategoryViewSet(ModelViewSet):
    """用户收藏类别视图"""
    serializer_class = CollectCategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['resource_id'] = self.request.query_params.get('resource_id', None)
        context['user_id'] = self.request.user.id
        return context

    def get_queryset(self):
        return CollectCategory.objects.filter(user_id=self.request.user.id).all()

    @transaction.atomic()
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        CollectRedisModel(self.request.user.id, instance.id).delete()


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
        'list': PostSerializer
    }
    c_serializer_class = CreateCollectSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    pagination_class = LimitOffsetPagination
    filter_class = None
    search_fields = ('name',)

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if not category_id:
            raise ValidationError({'success': False,
                                   'code': RET.PARAMERR,
                                   'msg': error_map[RET.PARAMERR]})
        self.collect_dict = CollectRedisModel(self.request.user.id, category_id).get_all(self.request)
        collect_resource_ids = self.collect_dict.keys()
        return field_sort_queryset(Post, collect_resource_ids)

    def paginate_queryset(self, queryset):
        queryset_list = super().paginate_queryset(queryset)
        for i in queryset_list:
            date_array = datetime.datetime.fromtimestamp(self.collect_dict.get(i.id))
            i.created_time = date_array.strftime("%Y-%m-%d %H:%M")
        return queryset_list

    @transaction.atomic()
    def perform_create(self, serializer):
        attr = serializer.save()
        after_collect.delay(**attr)


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
        return field_sort_queryset(User, focus_ids)

    def get_serializer_class(self):
        if self.action == 'create':
            return self.c_serializer_class
        return self.r_serializer_class

    def get_permissions(self):
        if self.action != 'create':
            return []
        return super().get_permissions()
