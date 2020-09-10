# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/5 15:31
from django.conf import settings

from celery import shared_task
from django.db import transaction
from django_celery_results.models import TaskResult


@shared_task()
def clear_celery_results():
    with transaction.atomic():
        result = TaskResult.objects.get_all_expired(settings.CELERY_RESULT_EXPIRES)
        mod_row = result.update(worker='DELETE')
    return mod_row


@shared_task()
def real_clear_celery_results():
    with transaction.atomic():
        del_row = TaskResult.objects.filter(worker='DELETE').delete()
    return del_row


