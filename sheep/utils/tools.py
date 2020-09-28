# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/26 23:33
import os
import re
import uuid
import time
import json
import itertools
import datetime
from collections import Iterable, Mapping
from decimal import Decimal, ROUND_HALF_UP
from typing import Union

from xpinyin import Pinyin

pin = Pinyin()


def covertFileSize(size):
    """
    kb转为人性化输出
    :param size:
    :return:
    """
    kb = 1
    mb = kb * 1024
    gb = mb * 1024
    tb = gb * 1024
    if size >= tb:
        return "%.1f TB" % float(size / tb)
    elif size >= gb:
        return "%.1f GB" % float(size / gb)
    elif size >= mb:
        return "%.1f MB" % float(size / mb)
    elif size >= kb:
        return f"{size // kb} KB"


def getFlattenOne(arr: Iterable) -> Iterable:
    """
    获取扁平数组的第一个数组
    :param arr:
    :return:
    """
    arr=list(itertools.chain(*arr))
    return arr[0] if len(arr) else None


def getFlatten(items: list) -> list:
    """
    数组扁平化
    :param items:
    :return:list
    """
    items = json.dumps(items)
    return json.loads('[' + re.sub(r'[\[\]]', '', items) + ']')


def random_filename(filename: str)->str:
    """
    随机文件名
    :param filename: 原始文件名称
    :return: uuid之后的新文件名称
    """
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def get_day_zero_time() ->tuple:
    """
    获取到今日凌晨的秒数
    :return: 当前时间到今日凌晨所剩的秒数
    """
    now=datetime.datetime.now()
    date_zero = datetime.datetime.now().replace(year=now.year, month=now.month,
                                            day=now.day, hour=23, minute=59, second=59)
    date_zero_time = time.mktime(date_zero.timetuple())
    return now.strftime('%Y-%m-%d'),round(date_zero_time-time.time())


def sort_pinyin(queryset: Iterable)->dict:
    """
    根据用户名称的首字母进行分类
    :param queryset:
    :return: 返回字典{'a':[],'b':[]}
    """
    dic={}
    for i in queryset:
        user_dict=i[0].to_dict()
        userCheck=i[1].to_dict()
        pinyin = pin.get_pinyin(userCheck['remark'])[0]  # 以备注作为分组
        dic.setdefault(pinyin,[])
        user_dict['is_friend'] = True
        user_dict['pinyin']=pinyin
        user_dict['user']=userCheck
        dic[pinyin].append(user_dict)
    return dict(sorted(dic.items(),key=lambda x:x[0]))


def stdout(s: str):
    """
    输出
    :param s: 字符串
    :return:
    """
    print(s.center(50, '*'))


def rounding(num: Union[str, Decimal], reserve_decimal: str = '0.0') -> Decimal():
    """
    四舍五入
    :param num:数字
    :param reserve_decimal: 保留几位小数
    :return:
    """
    if isinstance(num, (int, float)):
        num = str(num)
    return Decimal(num).quantize(Decimal(reserve_decimal), rounding=ROUND_HALF_UP)


if __name__ == '__main__':
    now=datetime.datetime.now()
    print(now.strftime('%Y-%m-%d %H:%M:%S'))
