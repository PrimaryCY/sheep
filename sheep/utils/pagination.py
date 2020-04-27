# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/18 13:28
from rest_framework.pagination import LimitOffsetPagination as DRF_LimitoffsetPagination


class LimitOffsetPagination(DRF_LimitoffsetPagination):
    #默认显示的个数
    default_limit = 2
    #当前的位置
    offset_query_param = "offset"
    #通过limit改变默认显示的个数
    limit_query_param = "limit"
    #一页最多显示的个数
    max_limit = 10