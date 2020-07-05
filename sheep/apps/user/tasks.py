# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/4 20:10
import time

from celery import shared_task

from apps.user.models import User


@shared_task()
def test():
    time.sleep(5)
    print(User.objects.all().first().username)
    print('finish')