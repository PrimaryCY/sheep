# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/4 19:36
from __future__ import absolute_import, unicode_literals

import os
import logging; logger = logging.getLogger('celery_logger')

from celery import Celery
from celery.signals import task_success, task_failure
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheep.settings')
os.environ['CELERY_RDB_HOST'] = '0.0.0.0'

app = Celery("sheep")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS)


# 配置日志
@task_success.connect
def task_success_log(sender=None, headers=None, body=None, result=None, **kwargs):
    logger.info('*'*80)
    logger.info(f'sender:{sender.name}---id:{sender.request.id} success')
    logger.info(f'headers:{headers}')
    logger.info(f"body:{body}")
    logger.info(f"kwargs:{kwargs}")
    logger.info(f'result:{result}')
    logger.info('*'*80)


@task_failure.connect
def task_failure_log(sender=None, headers=None, body=None,**kwargs):
    logger.error('*'*80)
    logger.error(f'sender:{sender.name}---id:{kwargs["task_id"]}')
    logger.error(f'headers:{headers}')
    logger.error(f'body:{body}')
    logger.error(f'args:{kwargs["args"]}')
    logger.error(f'kwargs:{kwargs["kwargs"]}')
    logger.exception(f'traceback{kwargs["traceback"]}')
    logger.error('*'*80)


# 启动flower
# celery flower -A sheep.celery --persistent=True

# linux:
# celery -B -A sheep.celery worker -l info

# windows:
# celery -A sheep.celery beat
# celery -A sheep.celery worker -l info --pool=eventlet
