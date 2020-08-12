# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/14 20:18
from django.db.models.signals import ModelSignal

pre_ud_save = ModelSignal(providing_args=["sender", "queryset", 'request'],
                          use_caching=True)
aft_ud_save = ModelSignal(providing_args=["sender", "queryset", 'request'], use_caching=True)
