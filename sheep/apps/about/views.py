from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers

from apps.about.models import About
from sheep.constant import RET, error_map
from utils.drf_extensions.decorators import only_data_cache_response


class AboutUsViewSet(GenericViewSet):
    """关于我们"""
    permission_classes = ()

    @only_data_cache_response()
    def list(self, request, *args, **kwargs):
        data = About.objects.first().content
        return Response(data)
