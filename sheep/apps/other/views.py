from rest_framework.generics import CreateAPIView, ListCreateAPIView

from apps.other.serializer import UploadSerializer
from apps.other.models import UploadHistoryModel


class UploadViewSet(ListCreateAPIView):
    """上传文件视图"""
    serializer_class = UploadSerializer
    permission_classes = ()
    queryset = UploadHistoryModel.objects.all()
