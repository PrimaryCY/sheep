# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/10 17:43
from typing import Mapping

from django.utils.deprecation import MiddlewareMixin

from apps.user.authentication import TokenAuthentication
from sheep.constant import RET


class DRFCodeMiddleware(MiddlewareMixin):
    """处理drf响应middleware"""

    def process_template_response(self, request, response):
        return self.process_response(request, response)

    def process_response(self, request, response):
        exc = getattr(response, 'exception', None)
        # 500的情况
        if exc is None:
            return response
        # 正常返回的情况
        if exc is False:
            self.success_response_handle(response)
        # 预料中的异常的异常情况
        else:
            self.error_response_handle(request, response)
        return response

    @staticmethod
    def success_response_handle(response):
        """无异常正常返回时"""
        if isinstance(response.data, list)\
                or {'code', 'data'} - set(response.data.keys()):
            response.data = {
                'success': True,
                'code': RET.OK,
                'data': response.data
            }
        return response

    def error_response_handle(self, request, response):
        """正常报错返回"""
        c = response.status_code

        # 特殊状态处理映射
        error_dict = {
            400: self.error_400_handle,     # serializer内抛出的异常
            401: self.error_401_handle,     # token失效的异常
        }
        # 特定的几种状态处理
        if c in error_dict.keys():
            error_dict.get(c)(response)
        # 当报错返回数据没有包含code,success,msg关键状态
        if {'code', 'msg'} - set(response.data.keys()):
            response.data = {
                'success': False,
                'code': response.status_code,
                'msg': response.data.get('detail', '没有报错提示!')
            }

        response.data['status'] = response.status_code
        response.status_code = 200

    @staticmethod
    def error_400_handle(response):
        """
        特定报错状态处理
        使用原生django的validators时候 URLValidator(message='头像地址不正确!')只能传入str,传入dict无效
        """
        # 在validate方法中的报错会没有字段名称显示
        if not {'code', 'msg'} - set(response.data.keys()):
            response.data['success'] = False
            response.data = {k: v[0] if isinstance(v, list) else v for k, v in response.data.items()}
            return
        for field, res_msg in response.data.copy().items():
            error_msg = dict()
            if isinstance(res_msg, Mapping):
                # 如果报错信息是dict形式
                s, c, m = res_msg.get('success', False), res_msg.get('code', RET.PARAMERR), res_msg.get('msg')
                error_msg['success'] = s[0] if isinstance(s, list) else s
                error_msg['code'] = c[0] if isinstance(c, list) else c
                error_msg['msg'] = m[0] if isinstance(m, list) else m
            else:
                # 如果报错信息是list或者str,也就是serializer原始默认的报错
                error_msg['success'] = False
                error_msg['code'] = RET.PARAMERR
                res_msg = res_msg[0] if len(res_msg) else ""
                error_msg['msg'] = res_msg
            response.data = error_msg
            break

    @staticmethod
    def error_401_handle(response):
        response.delete_cookie(TokenAuthentication.token_name)
