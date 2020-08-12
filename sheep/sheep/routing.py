# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/6/9 19:17

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler

from sheep.init_server import server
import api.routing

application = ProtocolTypeRouter({
    'http': AsgiHandler,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            api.routing.websocket_urlpatterns# 指明路由文件是api/routing.py
        )
    ),
})

server.init()


