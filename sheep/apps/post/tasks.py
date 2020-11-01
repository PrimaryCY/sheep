# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/9/9 14:34
from typing import Iterable

from celery import shared_task

from apps.post.models import Post, PostReply
from apps.operate.models import BrowsingHistoryRedisMode, UserDynamic


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
    qs = Post.objects.filter(praise_num__lt=-50)
    qs.update(status=3)
    for i in qs:
        after_delete_post(user_id=i.author_id, ip='', resource_id=i.id)


@shared_task()
def after_create_post_reply(post_id: int, user_id: int, id: int, ip: str):
    """
    增加回复之后操作
    :param post_id:
    :param user_id:
    :param id:
    :param ip:
    :return:
    """
    Post.add_post_num(post_id, user_id)
    UserDynamic.add_create_reply_dynamic(user_id=user_id, resource_id=id, ip=ip)


@shared_task()
def after_delete_post_reply(post_id: int, user_id: int, id: int, ip: str):
    """
    删除回复之后操作
    :param post_id:
    :param user_id:
    :param id:
    :param ip:
    :return:
    """
    Post.del_post_num(post_id)
    UserDynamic.delete_reply_dynamic(user_id=user_id, resource_id=id, ip=ip)


@shared_task()
def after_list_reply(user_id: int, ids:Iterable):
    """
    修改文章已读未读状态
    :param user_id:
    :param ids:
    :return:
    """
    PostReply.objects.filter(id__in=ids, replier_id=user_id, is_read=False).update(is_read=True)


@shared_task()
def after_create_post(user_id, ip, resource_id):
    """
    创建文章/提问之后
    :param user_id:
    :param ip:
    :param resource_id:
    :return:
    """
    UserDynamic.add_create_post_dynamic(user_id, ip, resource_id)


@shared_task()
def after_update_post(user_id, ip, resource_id):
    """
    创建文章/提问之后
    :param user_id:
    :param ip:
    :param resource_id:
    :param other:
    :return:
    """
    UserDynamic.add_update_post_dynamic(user_id, ip, resource_id)


@shared_task()
def after_delete_post(user_id, ip, resource_id):
    """
    删除文章/提问之后
    :param user_id:
    :param ip:
    :param resource_id:
    :return:
    """
    UserDynamic.delete_post_dynamic(user_id, resource_id, ip)
