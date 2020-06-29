# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/6/29 20:17
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import CacheResponse


class OnlyDataCacheResponse(CacheResponse):

    def process_cache_response(self,
                               view_instance,
                               view_method,
                               request,
                               args,
                               kwargs):
        key = self.calculate_key(
            view_instance=view_instance,
            view_method=view_method,
            request=request,
            args=args,
            kwargs=kwargs
        )
        data = self.cache.get(key)
        if not data:
            response = view_method(view_instance, request, *args, **kwargs)

            if not response.status_code >= 400 or self.cache_errors:
                self.cache.set(key, response.data, self.timeout)
        else:
            response = Response(data=data)

        if not hasattr(response, '_closable_objects'):
            response._closable_objects = []

        return response


only_data_cache_response = OnlyDataCacheResponse
