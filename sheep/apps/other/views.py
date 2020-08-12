from django.conf import settings
from django_celery_results.models import TaskResult
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from apps.other.serializer import UploadHistorySerializer, OptionSerializer, FeedbackCategorySerializer, \
    ListFeedbackSerializer, CreateFeedbackSerializer, UpdateFeedbackSerializer, CeleryResultsSerializer, UploadTokenSerializer
from apps.other.filters import FeedbackFilter, UploadHistoryFilter
from apps.other.models import UploadHistoryModel, Feedback, FeedbackCategory
from apps.user.permission import IsLoginUser, IsAdminUser
from sheep.constant import RET
from utils.drf_extensions.decorators import only_data_cache_response
from utils.viewsets import ModelViewSet, ReadOnlyModelViewSet
from utils.mixins import CreateModelMixin
from utils.pagination import LimitOffsetPagination
from utils.qiniu.cache import QiNiuCacheResponse


class UploadTokenViewSet(CreateModelMixin,
                         GenericViewSet):
    """获取七牛云token视图"""
    serializer_class = UploadTokenSerializer
    permission_classes = ()

    @QiNiuCacheResponse(timeout=settings.QI_NIU_CLOUD.get('expires')-200)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        data = {"success": True, "code": RET.OK, "data": serializer.data}
        res = Response(data, status=200, headers=headers)
        return res


class UploadHistoryViewSet(GenericViewSet,
                            ListModelMixin,
                            CreateModelMixin):
    """上传文件历史纪录视图"""
    pagination_class = LimitOffsetPagination
    serializer_class = UploadHistorySerializer
    permission_classes = ()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = UploadHistoryFilter
    filter_fields = ('user_id', 'url')
    ordering_fields = "__all__"
    queryset = UploadHistoryModel.objects.all()


class OptionViewSet(GenericViewSet):
    """公共配置"""
    serializer_class = OptionSerializer
    permission_classes = ()
    queryset = ' '

    @only_data_cache_response()
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset)
        return Response(serializer.data)


class FeedbackCategoryViewSet(ModelViewSet):
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer

    def get_permissions(self):
        if self.request.method.lower() == 'get':
            return []
        return [IsAdminUser()]


class FeedbackViewSet(ModelViewSet):
    serializer_class = {
        'list': ListFeedbackSerializer,
        'retrieve': ListFeedbackSerializer,
        'create': CreateFeedbackSerializer,
        'update': UpdateFeedbackSerializer,
        'partial_update': UpdateFeedbackSerializer
    }
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = FeedbackFilter
    search_fields = ('desc',)
    ordering_fields = ('create_time',)
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return []
        else:
            return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Feedback.objects.all()
        else:
            return Feedback.objects.filter(author_id=user.id).all()


class CeleryResultsViewSet(ReadOnlyModelViewSet):
    """celery-worker执行结果"""
    serializer_class = CeleryResultsSerializer
    queryset = TaskResult.objects.all()
    permission_classes = (IsAdminUser,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('status', 'task_name', 'worker')
    search_fields = ('task_id',)
    order_fields = ('date_created', 'date_done')
