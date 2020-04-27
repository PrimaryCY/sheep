# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/6 15:33
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from sheep.constant import RET, error_map


class IsAdminUser(BasePermission):
    """
    admin用户拥有的权限
    """
    message = {'code': RET.ROLEERR, 'success': False, 'msg': error_map[RET.ROLEERR]}

    def has_permission(self, request, view):
        # 这里增加判断是为了兼容rest framework的可视化界面不报错
        if hasattr(request.user, 'is_anonymity'):
            return bool(request.user and request.user.is_admin)


class IsLoginUser(BasePermission):
    """
    登录之后才拥有的权限
    """
    message = {'code': RET.ROLEERR, 'success': False, 'msg': error_map[RET.ROLEERR]}

    def has_permission(self, request, view):
        # 这里增加判断是为了兼容rest framework的可视化界面不报错
        if hasattr(request.user, 'is_anonymity'):
            return not request.user.is_anonymity

