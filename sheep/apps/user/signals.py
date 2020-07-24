# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/14 19:24
from apps.user.models import User
from utils.django_util.signals import aft_ud_save
from django.dispatch import receiver


@receiver(aft_ud_save, sender=User)
def test_signals(sender, queryset=None, **kwargs):
    # print(queryset)
    # print(sender)
    pass
