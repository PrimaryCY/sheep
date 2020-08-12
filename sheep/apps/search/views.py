from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet

from apps.post.models import Post
from apps.post.serializer import PostSerializer
from apps.search.filters import SearchPostFilter
from utils.pagination import LimitOffsetPagination
from utils.viewsets import ExtensionViewMixin


class SearchViewSet(ExtensionViewMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """所有帖子视图"""
    serializer_class = {
        'list': PostSerializer,
    }
    permission_classes = ()
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    queryset = Post.objects.all()
    filter_class = SearchPostFilter
    search_fields = ('name', 'desc')

