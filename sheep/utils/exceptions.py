# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/11/29 15:41
from typing import Mapping

from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


class CodeError(ValidationError):

    def __init__(self, code=4003, message=None, success=False, **kwargs):
        """自定义code报错类"""
        self.detail = dict()
        self.detail['code'] = code
        self.detail['message'] = message
        self.detail['success'] = success
        self.detail.update(kwargs)


class ExceptionHandle(object):

    @staticmethod
    def ValidationError_handle(response, context):
        """处理validationError的报错信息"""
        serializer = context['view'].get_serializer(data=context['request'].data)
        for field in serializer._writable_fields:
            if response.data.get(field.field_name):
                error_msg = dict()
                res_msg = response.data.get(field.field_name)
                if isinstance(res_msg, Mapping):
                    # 如果报错信息是dict形式
                    error_msg['success'] = res_msg.get('success', False)
                    error_msg['code'] = res_msg.get('code', 4003)
                    error_msg['msg'] = res_msg.get('msg')
                else:
                    # 如果报错信息是list或者str,也就是serializer原始默认的报错
                    error_msg['success'] = False
                    error_msg['code'] = 4003
                    res_msg = res_msg[0] if len(res_msg) else ""
                    error_msg['msg'] = res_msg
                response.data = error_msg
                break

    def exceptions_handle(self, exc, context):
        """
        自定义异常处理,
        1.重置每个异常响应的返回格式 --> {'code': 4003, 'msg': '用户名不符合规范', 'success': True}
        2.将序列号过程中exc详情从list变为str
        """
        response = exception_handler(exc, context)

        if response is None:
            return response

        if isinstance(exc, CodeError):
            response.data = exc.detail
        elif isinstance(exc, ValidationError):
            self.ValidationError_handle(response, context)
        self.common_exceptions_handle(response)
        return response

    @staticmethod
    def common_exceptions_handle(response):
        response.data['status_code'] = response.status_code


def main(exc, response):
    return ExceptionHandle().exceptions_handle(exc, response)
