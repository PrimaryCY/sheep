# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/6/29 15:14
import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django')


class RecordLoggingMiddleware(MiddlewareMixin):
    """
    记录日志错误,
    连接上sentry后取消该中间件
    """

    def process_template_response(self, request, response):
        response = self.process_response(request, response)
        return response

    def process_response(self, request, response):
        exc = getattr(response, 'exception', None)
        # 500的情况
        if exc is None:
            user = getattr(request, 'user', None)
            user_id = getattr(user, 'id', '未登录')
            username = getattr(user, 'username', '未登录')
            logger.error(f'user:{user_id}-{username}')
            logger.error(f'body:{request.body.decode()}')
        return response
