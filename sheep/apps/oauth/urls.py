# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/10/13 18:23
from django.urls import include, path

from utils.routes import CustomRouter
from apps.oauth.views import ApplicationViewSet, OauthTokenView, OauthRegisterView

router = CustomRouter()
# 上传接口
router.register('applications', ApplicationViewSet, basename='applications')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'token/', OauthTokenView.as_view()),
    path(r'register/', OauthRegisterView.as_view())
]
