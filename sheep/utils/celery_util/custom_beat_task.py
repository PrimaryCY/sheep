# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/9/15 20:11

from datetime import timedelta

from celery import shared_task
from django.utils.module_loading import import_string
from urllib3.util import current_time


@shared_task()
def interval(func, seconds, args=(), task_id=None):
    """
    动态添加定时任务
    :param func: 任务函数的路径
    :param seconds: 定时的时间
    :param args: 任务的参数
    :param task_id: 任务id
    :return:
    """
    next_run_time = current_time() + timedelta(seconds=seconds)
    kwargs = dict(args=(func, seconds, args), eta=next_run_time)
    if task_id is not None:
        kwargs.update(task_id=task_id)
    interval.apply_async(**kwargs)
    func = import_string(func)
    return func(*args)
