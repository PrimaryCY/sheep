# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/4 20:10
import copy
import time
import datetime
import requests
from requests.exceptions import RequestException

from celery import shared_task
from celery.contrib import rdb
from django.conf import settings
from django.db.models import F

from apps.user.models import User


@shared_task()
def test(arg=1):
    result = None
    # 断点调试
    rdb.set_trace()
    print(User.objects.all().first().username)
    print('finish')
    return result


@shared_task()
def send_bd_location_ip(params):
    """获取ip真实地址"""
    try:
        res = requests.get(settings.BD_API_LOCATION_IP_URL, params=params,
                           timeout=settings.BD_API_TIMEOUT)
    except RequestException:
        return None
    data = res.json()
    if res.status_code == 200 and data['status'] == 0:
        return data


@shared_task()
def after_login(user_id, ip):
    """
    用户成功登录后的操作
    :return:
    """
    user = User.objects.filter(id=user_id).only('is_anonymity', 'last_login_province').first()
    update_dict = {
        'login_num': F('login_num') + 1,
        'last_login': datetime.datetime.now()
    }
    if not user.last_login_province or not user.is_anonymity:
        params = copy.copy(settings.BD_API_MAP_PARAMS)
        params['ip'] = ip if ip != '127.0.0.1' else ''
        data = send_bd_location_ip.delay(params=params).get()
        if data:
            addr_detail = data['content']['address_detail']
            update_dict['last_login_province'] = addr_detail['province']
            update_dict['last_login_city'] = addr_detail['city']

    User.objects.filter(id=user_id).update(**update_dict)

    update_dict.pop('login_num')
    return update_dict
