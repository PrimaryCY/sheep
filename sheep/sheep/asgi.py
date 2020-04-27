# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/11/15 11:13
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import api.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            api.routing.websocket_urlpatterns# 指明路由文件是api/routing.py
        )
    ),
})


from apps.post.models import Category

Category.create_default_category()
