# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/22 15:48
import json
import hashlib

from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import CacheResponse


class QiNiuCacheResponse(CacheResponse):

    def process_cache_response(self,
                               view_instance,
                               view_method,
                               request,
                               args,
                               kwargs):
        key = self.generate_key(request)
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

    @staticmethod
    def generate_key(request):
        """ 加密影响性能.去除"""
        # hl = hashlib.md5()
        # hl.update(json.dumps(request.data).encode(encoding='utf-8'))
        # return hl.hexdigest()
        return f'qiniu_{request.data.get("bucket", None)}'


qi_niu_cache_response = QiNiuCacheResponse