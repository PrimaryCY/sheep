# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/31 15:14
from celery import shared_task

from apps.operate.models import Collect


@shared_task()
def after_collect(category_id, resource_id, is_active, *args, **kwargs):
    """
    收藏与删除删除或增加对应的read_num | total
    :param type:
    :param category_id:
    :param resource_id:
    :param is_active:
    :param args:
    :param kwargs:
    :return:
    """
    Collect.after_collect(category_id,
                          resource_id,
                          is_active)
