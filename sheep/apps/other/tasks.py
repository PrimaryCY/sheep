# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/5 15:31
from django.conf import settings

from celery import shared_task
from django_celery_results.models import TaskResult


@shared_task()
def clear_celery_results():
    TaskResult.objects.delete_expired(settings.CELERY_RESULT_EXPIRES)
