# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/4/5 15:52
from collections import deque

from rest_framework.routers import DefaultRouter
from rest_framework.routers import Route


class CustomRouter(DefaultRouter):

    extra_routes = deque([
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                # 外层url使用put
                'put': 'bulk_update',
                'patch': 'bulk_partial_update',
                'delete': 'bulk_delete'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'update'}
        )]
    )

    def __init__(self, *args, **kwargs):
        self.extra_routes.extend(self.routes)
        self.routes=self.extra_routes
        super().__init__(*args,**kwargs)