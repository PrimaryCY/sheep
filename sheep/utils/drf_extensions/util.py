# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/7/11 21:04
from .key_constructor.constructors import LimitOffsetListKeyConstructor

# 补充limit_offset分页类的缓存key
limit_offset_list_cache_key_func = LimitOffsetListKeyConstructor()
