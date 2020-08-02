# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/31 15:14
from celery import shared_task

from apps.operate.models import Collect, CollectRedisModel


@shared_task()
def after_delete_user_category(user_id, category_id):
    """
    删除收藏集之后,删除redis中对应的key
    :param user_id:
    :param category_id:
    :return:
    """
    CollectRedisModel(user_id, category_id).delete()


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
