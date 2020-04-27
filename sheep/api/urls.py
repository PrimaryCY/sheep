# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/11/14 16:13
from django.conf.urls import include, url

urlpatterns = [
    url(r'v1/', include(('api.v1.v1', 'api.v1.v1'), namespace='v1')),
]

