# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/11/14 16:15
from django.conf.urls import url, include

from utils.routes import CustomRouter
from apps.other.views import UploadViewSet
from apps.other.views import OptionViewSet

router = CustomRouter()
# 上传接口
router.register('upload', UploadViewSet, base_name='upload')
# 公共配置
router.register('option', OptionViewSet, base_name='option')

urlpatterns = [
    url(r'web/', include(('api.v1.web', 'api.v1.v1.web'), namespace='web')),
    url(r'', include(router.urls))
]
