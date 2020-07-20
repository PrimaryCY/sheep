"""sheep URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve
from django.conf import settings

import api.urls

urlpatterns = [
                  # 修改media文件路由
                  path(r'media/<path:path>/', serve, {"document_root": settings.MEDIA_ROOT}),
                  # 导入rest framework
                  path(r'api_auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path(r'api/', include(api.urls)),
              ] + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
