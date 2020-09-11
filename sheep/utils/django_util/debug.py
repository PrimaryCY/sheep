# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/6/29 15:14
from redis.client import StrictRedis

from celery.contrib import rdb
from django.conf import settings
from django_redis import get_redis_connection


def pdb_debug():
    """
    debug调试
    :return:
    """
    con: StrictRedis = get_redis_connection()
    if getattr(settings, 'PDB_DEBUG', False) and con.get('pdb'):
        rdb.set_trace()
