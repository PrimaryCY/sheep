# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/18 15:16
RdAllot = {
    1: '默认',
    2: 'restframework-extengsions',
    3: 'celery',
    10: '存储token',
}


class RET:
    OK                  = 2000
    NODATA              = 4002
    DATAEXIST           = 4003
    DATAERR             = 4004
    TOKENERR            = 4101
    LOGINERR            = 4102
    PARAMERR            = 4103
    USERERR             = 4104
    ROLEERR             = 4105
    PWDERR              = 4106
    REQERR              = 4201
    IPERR               = 4202
    THIRDERR            = 4301
    IOERR               = 4302
    DBERR               = 5001
    SERVERERR           = 5500
    UNKOWNERR           = 6000

error_map = {
    RET.OK                    : u"成功",
    RET.DBERR                 : u"数据库查询错误",
    RET.NODATA                : u"无数据",
    RET.DATAEXIST             : u"数据已存在",
    RET.DATAERR               : u"数据错误",
    RET.TOKENERR              : u"用户登录失效",
    RET.LOGINERR              : u"用户登录失败",
    RET.PARAMERR              : u"参数错误",
    RET.USERERR               : u"用户不存在或未激活",
    RET.ROLEERR               : u"用户无权限",
    RET.PWDERR                : u"密码错误",
    RET.REQERR                : u"非法请求或请求次数受限",
    RET.IPERR                 : u"IP受限",
    RET.THIRDERR              : u"第三方系统错误",
    RET.IOERR                 : u"文件读写错误",
    RET.SERVERERR             : u"服务器错误",
    RET.UNKOWNERR             : u"未知错误",
}