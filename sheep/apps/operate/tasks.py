# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/31 15:14
from celery import shared_task
from django.db.models import F
from django.db.utils import IntegrityError
from django.conf import settings

from apps.operate.models import Collect, CollectRedisModel, Praise
from apps.user.models import User
from apps.post.models import Post


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


@shared_task()
def after_praise_or_trample(operation: int, user_id: int, resource_id: int, praise_or_trample: int, t: int):
    """
    点赞redis之后的持久化到mysql操作,并且修改对应资源的praise总数
    :param user_id:
    :param resource_id:
    :param operation:
    :param praise_or_trample:
    :param t:
    :return:
    """
    model = Praise.PRAISE_TYPE_MODEL_MAPPING[t]
    model.objects.filter(id=resource_id).update(praise_num=F('praise_num')+operation)
    # 匿名用户不持久化到mysql
    if User.objects.filter(id=user_id, is_anonymity=True).exists():
        return

    if praise_or_trample == 0:
        Praise.objects.filter(user_id=user_id, t=t, resource_id=resource_id).delete()
    else:
        with settings.LOCK_REDIS.lock(f'{user_id}-{resource_id}-{t}') :
            Praise.objects.update_or_create(defaults={
                'praise_or_trample': praise_or_trample
            }, user_id=user_id, resource_id=resource_id, t=t)
