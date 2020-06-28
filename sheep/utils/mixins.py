from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.utils.encoding import force_text
from rest_framework import status
from rest_framework_extensions.settings import extensions_api_settings
from rest_framework_extensions import utils





class CreateModelMixin(object):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateModelMixin(object):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class BulkOperationBaseMixin(object):
    def is_object_operation(self):
        return bool(self.get_object_lookup_value())

    def get_object_lookup_value(self):
        return self.kwargs.get(getattr(self, 'lookup_url_kwarg', None) or self.lookup_field, None)

    def is_valid_bulk_operation(self):
        if extensions_api_settings.DEFAULT_BULK_OPERATION_HEADER_NAME:
            header_name = utils.prepare_header_name(extensions_api_settings.DEFAULT_BULK_OPERATION_HEADER_NAME)
            return bool(self.request.META.get(header_name, None)), {
                'detail': 'Header \'{0}\' should be provided for bulk operation.'.format(
                    extensions_api_settings.DEFAULT_BULK_OPERATION_HEADER_NAME
                )
            }
        else:
            return True, {}


class ListDestroyModelMixin(BulkOperationBaseMixin):
    def delete(self, request, *args, **kwargs):
        if self.is_object_operation():
            return super(ListDestroyModelMixin, self).destroy(request, *args, **kwargs)
        else:
            return self.destroy_bulk(request, *args, **kwargs)

    def destroy_bulk(self, request, *args, **kwargs):
        is_valid, errors = self.is_valid_bulk_operation()
        if is_valid:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = self.pre_delete_bulk(queryset)  # todo: test and document me
            queryset.update(is_active=False)
            self.post_delete_bulk(queryset)  # todo: test and document me
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def pre_delete_bulk(self, queryset):
        """
        Placeholder method for calling before deleting an queryset.
        """
        ids = self.request.GET.get("ids", '')
        id_list = ids.split(",")
        queryset = queryset.filter(id__in=id_list)
        return queryset

    def post_delete_bulk(self, queryset):
        """
        Placeholder method for calling after deleting an queryset.
        """
        pass


class ListUpdateModelMixin(BulkOperationBaseMixin):
    def patch(self, request, *args, **kwargs):
        if self.is_object_operation():
            return super(ListUpdateModelMixin, self).partial_update(request, *args, **kwargs)
        else:
            return self.partial_update_bulk(request, *args, **kwargs)

    def partial_update_bulk(self, request, *args, **kwargs):
        is_valid, errors = self.is_valid_bulk_operation()
        if is_valid:
            queryset = self.filter_queryset(self.get_queryset())
            update_bulk_dict = self.get_update_bulk_dict(serializer=self.get_serializer_class()(), data=request.data)
            queryset = self.pre_save_bulk(queryset, update_bulk_dict)  # todo: test and document me
            try:
                queryset.update(**update_bulk_dict)
            except ValueError as e:
                errors = {
                    'detail': force_text(e)
                }
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            self.post_save_bulk(queryset, update_bulk_dict)  # todo: test and document me
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def get_update_bulk_dict(self, serializer, data):
        update_bulk_dict = {}
        for field_name, field in serializer.fields.items():
            if field_name in data and not field.read_only:
                update_bulk_dict[field.source or field_name] = data[field_name]
        return update_bulk_dict

    def pre_save_bulk(self, queryset, update_bulk_dict):
        """
        Placeholder method for calling before deleting an queryset.
        """
        ids = self.request.GET.get("ids", '')
        id_list = ids.split(",")
        queryset = queryset.filter(id__in=id_list)
        return queryset

    def post_save_bulk(self, queryset, update_bulk_dict):
        """
        Placeholder method for calling after deleting an queryset.
        """
        pass


