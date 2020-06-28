# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/11/14 16:15
from django.conf.urls import url, include

from utils.routes import CustomRouter
from apps.other.views import UploadViewSet, FeedbackCategoryViewSet, FeedbackViewSet
from apps.other.views import OptionViewSet

router = CustomRouter()
# 上传接口
router.register('upload', UploadViewSet, basename='upload')
# 公共配置
router.register('option', OptionViewSet, basename='option')
# 意见反馈类别
router.register('feedback_category', FeedbackCategoryViewSet, basename='feedback_category')
# 意见反馈
router.register('feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    url(r'web/', include(('api.v1.web', 'api.v1.v1.web'), namespace='web')),
    url(r'', include(router.urls))
]