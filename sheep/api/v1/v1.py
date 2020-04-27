# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/11/14 16:15
from django.conf.urls import url, include

from apps.other.views import UploadViewSet

urlpatterns = [
    url(r'web/', include(('api.v1.web', 'api.v1.v1.web'), namespace='web')),
    url(r'upload/', UploadViewSet.as_view())
]
