from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin

from apps.other.serializer import UploadSerializer, OptionSerializer
from apps.other.models import UploadHistoryModel
from utils.pagination import LimitOffsetPagination


class UploadViewSet(GenericViewSet,
                    ListModelMixin,
                    CreateModelMixin):
    """上传文件视图"""
    pagination_class = LimitOffsetPagination
    serializer_class = UploadSerializer
    permission_classes = ()
    queryset = UploadHistoryModel.objects.all()


class OptionViewSet(GenericViewSet):
    """公共配置"""
    serializer_class = OptionSerializer
    permission_classes = ()
    queryset = ' '

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset)
        return Response(serializer.data)
