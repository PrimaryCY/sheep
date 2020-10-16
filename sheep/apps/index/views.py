from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from apps.index.serializer import BannerSerializer, HotSerializer
from apps.post.models import Post
from apps.post.serializer import PostSerializer, RetrievePostSerializer
from utils.drf_extensions.decorators import only_data_cache_response
from utils.pagination import LimitOffsetPagination
from utils.viewsets import ReadOnlyModelViewSet
from utils.drf_extensions.util import limit_offset_list_cache_key_func


class BannerViewSet(GenericViewSet):
    """轮播图,点赞数最多的前5条"""
    serializer_class = BannerSerializer
    permission_classes = ()

    def get_queryset(self):
        return Post.objects.filter(image__isnull=False).order_by('-praise_num').values('id', 'image', 'name')[:5]

    @only_data_cache_response()
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class HotViewSet(ListModelMixin,
                 GenericViewSet):
    """热门,浏览数最多的前15条"""
    serializer_class = HotSerializer
    permission_classes = ()

    def get_queryset(self):
        return Post.objects.order_by('-read_num').values('id', 'name', 'post_type', 'read_num', 'image')[:10]

    @only_data_cache_response()
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


