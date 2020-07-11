# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/11 21:09
from rest_framework_extensions.key_constructor.bits import QueryParamsKeyBit, PaginationKeyBit


class LimitOffsetPaginationKeyBit(QueryParamsKeyBit):
    def get_data(self, **kwargs):
        kwargs['params'] = []
        if hasattr(kwargs['view_instance'], 'paginator'):
            if hasattr(kwargs['view_instance'].paginator, 'offset_query_param'):
                kwargs['params'].append(
                    kwargs['view_instance'].paginator.offset_query_param)
            if hasattr(kwargs['view_instance'].paginator,
                       'limit_query_param'):
                kwargs['params'].append(
                    kwargs['view_instance'].paginator.limit_query_param)
        return super(LimitOffsetPaginationKeyBit, self).get_data(**kwargs)
