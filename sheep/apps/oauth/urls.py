# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/10/13 18:23
from django.urls import include, path

from utils.routes import CustomRouter
from apps.oauth.views import ApplicationViewSet, OauthTokenView, OauthRegisterView, UserOauthViewSet

router = CustomRouter()
# 所有第三方应用接口
router.register('applications', ApplicationViewSet, basename='applications')
# 获取用户oauth信息接口
router.register('user_oauth', UserOauthViewSet, basename='user_oauth')

urlpatterns = [
    path(r'', include(router.urls)),
    # 交换access token接口
    path(r'token/', OauthTokenView.as_view()),
    # 绑定用户接口
    path(r'register/', OauthRegisterView.as_view())
]
