from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.index.serializer import IndexSerializer
from utils.drf_extensions.decorators import only_data_cache_response


class IndexViewSet(GenericViewSet):
    """首页"""
    serializer_class = IndexSerializer
    permission_classes = ()
    queryset = ['index', ]

    # @only_data_cache_response()
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset)
        return Response(serializer.data)
