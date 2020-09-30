from __future__ import unicode_literals

from typing import Mapping

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from utils.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


class SerializerContextViewMixin(object):

    def get_serializer(self, queryset=None, *args, **kwargs):
        many = kwargs.get('many', False)
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context(queryset, many=many)
        return serializer_class(queryset, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return super().get_serializer_context()


class ExtensionViewMixin(object):

    def get_serializer_class(self):
        if isinstance(self.serializer_class, Mapping):
            '''
            如果使用drf的模板渲染
            这里就不要用self.serializer_class = self.serializer_class.get('xx')
            要不然put或者patch的渲染都会选择post方法的serializer去渲染
            '''
            serializer_class = self.serializer_class.get(self.action)
        else:
            serializer_class = self.serializer_class
        assert serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )
        return serializer_class


class ModelViewSet(CreateModelMixin,
                   ExtensionViewMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    pass


class ReadOnlyModelViewSet(RetrieveModelMixin,
                           ExtensionViewMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass
