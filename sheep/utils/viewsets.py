from __future__ import unicode_literals

from typing import Mapping

from utils.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


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
