# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/6 15:56
import re


class ReCompile(object):
    # ipv4地址正则
    Ipv4 = re.compile(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
    # 特殊字符正则
    SpecialStr = re.compile("[`~!@#$%^&*()_\-+=<>?:\"{}|,.\/;'\\[\]·~！@#￥%……&*（）——\-+={}|《》？：“”【】、；‘’，。、]")
    # 邮箱正则
    Email = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$')
    # 手机号正则校验
    Phone = re.compile(r"^1[3456789]\d{9}$")
