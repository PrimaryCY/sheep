# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/4 19:36
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

# 为celery设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheep.settings')

# 创建应用
app = Celery("sheep")
app.config_from_object('django.conf:settings', namespace='CELERY')
# 设置app自动加载任务
# 从已经安装的app中查找任务
app.autodiscover_tasks(settings.INSTALLED_APPS)

# 启动flower
# celery flower -A sheep.celery --persistent=True

# linux:
# celery -B -A sheep.celery worker -l info

# windows:
# celery -A sheep.celery beat
# celery -A sheep.celery worker -l info --pool=eventlet
