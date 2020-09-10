# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/9/9 14:34
from celery import shared_task

from apps.post.models import Post
from apps.operate.models import BrowsingHistoryRedisMode


@shared_task()
def after_retrieve_post(resource_id, user_id, is_anonymity=False):
    Post.add_read_num(resource_id)

    # 不记录匿名用户的浏览记录
    if is_anonymity:
        return
    BrowsingHistoryRedisMode(user_id=user_id).create_history(resource_id=resource_id)


@shared_task()
def delete_trash_post():
    """
    定时删除垃圾文章删除
    :return:
    """
    Post.objects.filter(praise_num__lt=50).update(status=3)