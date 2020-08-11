# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/6/29 8:40
import os
import functools
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def init_stdout(s):
    s = f"{s} finish"

    def f(func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            func(*args, **kwargs)
            logger.info(s.center(50, '*'))
        return wrap
    return f


class InitServer(object):

    @init_stdout('media dir')
    def create_default_media_dir(self):
        """
        创建默认media目录
        :return:
        """
        if not hasattr(settings, 'MEDIA_DIRS'):
            return
        for dir in settings.MEDIA_DIRS:
            t = os.path.join(settings.MEDIA_ROOT, dir)
            if not os.path.isdir(t):
                os.makedirs(t)

    def init(self):
        """
        初始化服务准备工作
        :return:
        """
        # self.create_default_media_dir()
        from apps.post.models import Category
        from apps.other.models import FeedbackCategory
        from apps.user.models import User
        User.create_default_super_user()
        Category.create_default_category()
        FeedbackCategory.create_default_category()


server = InitServer()
