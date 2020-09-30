# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/9/9 14:34
from typing import Iterable

from celery import shared_task

from apps.post.models import Post, PostReply
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
    Post.objects.filter(praise_num__lt=-50).update(status=3)


@shared_task()
def after_create_post_reply(post_id: int, user_id:int):
    """
    增加帖子回复数量
    :param post_id:
    :param parent:
    :param user_id:
    :return:
    """
    Post.add_post_num(post_id, user_id)


@shared_task()
def after_delete_post_reply(post_id: int):
    """
    删除帖子回复数量
    :param post_id:
    :param parent:
    :return:
    """
    Post.del_post_num(post_id)


@shared_task()
def after_list_reply(user_id: int, ids:Iterable):
    """
    修改文章已读未读状态
    :param user_id:
    :param ids:
    :return:
    """
    PostReply.objects.filter(id__in=ids, replier_id=user_id, is_read=False).update(is_read=True)