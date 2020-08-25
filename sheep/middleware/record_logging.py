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
    def process_request(self, request):
        # drf只会调用httpRequest.read()方法，数据并不会保存到httpRequest.data中，从而会引发报错：RawPostDataException，不允许重复读取流
        # 手动调用一下，drf框架也不会重新读取流，也会继续用这个做的假io流
        request._body = request.body

    def process_exception(self, request, exc):
        logger.error('*'*95)
        user = getattr(request, 'user', None)
        user_id = getattr(user, 'id', '未登录')
        username = getattr(user, 'username', '未登录')
        logger.error(f'user:{user_id}-{username}')
        logger.error(f'body:{request.body}')
        logger.error('*'*95)
