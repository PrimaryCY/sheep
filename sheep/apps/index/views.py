from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from apps.index.serializer import BannerSerializer, HotSerializer
from apps.post.models import Post
from utils.drf_extensions.decorators import only_data_cache_response


class BannerViewSet(GenericViewSet):
    """轮播图,点赞数最多的前5条"""
    serializer_class = BannerSerializer
    permission_classes = ()
    queryset = Post.objects.filter(image__isnull=False).order_by('praise_num').values('id', 'image', 'name')[:5]

    @only_data_cache_response(timeout=120*60)
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


class HotViewSet(ListModelMixin,
                 GenericViewSet):
    """热门,浏览数最多的前15条"""
    serializer_class = HotSerializer
    permission_classes = ()
    queryset = Post.objects.order_by('read_num').values('id', 'name', 'post_type', 'read_num', 'image')[:10]

    @only_data_cache_response()
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)
