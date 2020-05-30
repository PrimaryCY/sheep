# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/11/27 18:39
import datetime
import inspect

from django.contrib.auth import get_user_model, _get_backends, user_login_failed, _clean_credentials
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, PermissionDenied
from django.db.models import Q

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django_redis import get_redis_connection

from sheep import settings
from sheep.constant import RET, error_map
from apps.user.token import Token

User = get_user_model()
user_redis = get_redis_connection('user')


class UserModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        用户登录验证
        :param request:
        :param username:
        :param password:
        :param kwargs:
        :return: True/False --> 用户登录成功失败标识
                user/msg --> 登录成功返回用户实例, 登录失败返回错误提示
        """
        try:
            user = User.objects.get(Q(Q(phone=username) | Q(email=username)) & Q(is_anonymity=False) & Q(is_active=True))
            code = kwargs.pop('code', None)
            # 验证码登录
            if code:
                res = user_redis.get()
                if res.decode('utf8') != code:
                    raise AuthenticationFailed('验证码错误!')
                if not user.is_phone:
                    user.is_phone = True
            # 密码登录
            elif not user.check_password(password):
                raise AuthenticationFailed('密码错误!')
        except ObjectDoesNotExist:
            return False, '邮箱或手机号不存在!'
        except MultipleObjectsReturned:
            return False, '服务器错误!'
        except AuthenticationFailed as ex:
            return False, ex.detail
        else:
            # 用户登录成功后的操作
            user.after_login(user)
            return True, user


class TokenAuthentication(BaseAuthentication):
    """
    rest framework权限验证
    """
    # token在客户端存储的key名
    token_name = settings.TOKEN.get('TOKEN_NAME')

    def authenticate(self, request):
        token = self.get_token(request)
        if not token:
            # 匿名用户处理
            user, t = self.anonymity_authenticate(request)
        else:
            # 登陆后用户处理
            user, t = self.user_authenticate(token, request)
        # 获取用户的ua
        user.ua = self.get_user_agent(request)
        return user, t

    @staticmethod
    def get_user_agent(request):
        """获取用户的ua"""
        ua = request.META.get('HTTP_USER_AGENT')
        if 'android'in ua or 'Linux' in ua:
            _user_agent = 'android'
        elif 'iphone' in ua:
            _user_agent = 'ios'
        else:
            _user_agent = 'pc'
        return _user_agent

    def get_token(self, request):
        """获取token"""
        return request.headers.get(self.token_name) or request.COOKIES.get(self.token_name, None)

    @staticmethod
    def anonymity_authenticate(request):
        """匿名用户"""
        remote_addr = request.META['REMOTE_ADDR']
        print(remote_addr)
        user, flag = User.objects.get_or_create(username=remote_addr, is_anonymity=True, is_active=True)
        # 匿名用户每次访问接口都会增加一次访问记录
        user.login_num += 1
        user.last_login = datetime.datetime.now()
        User.objects.filter(id=user.id).update(login_num=user.login_num,
                                               last_login=user.last_login)
        return user, flag

    @staticmethod
    def user_authenticate(token, request):
        """登录用户"""
        # 后门
        if token == '1234567890' and settings.DEVELOP:
            return User.objects.filter(id=1).first(), token

        user_info = Token.unpackTk(settings.TOKEN, request, token)

        if not user_info:
            raise AuthenticationFailed({'success': False, 'code': RET.TOKENERR, 'msg': error_map[RET.TOKENERR]})

        user = User.objects.filter(id=user_info.get('id')).first()
        if not user:
            raise AuthenticationFailed({'success': False, 'code': RET.USERERR, 'msg': error_map[RET.USERERR]})
        # 保存token解包数据结构, 退出登陆时使用
        user.user_info = user_info
        return user, token


def authenticate(request=None, **credentials):
    """
    重写authenticate方法
    """
    for backend, backend_path in _get_backends(return_tuples=True):
        try:
            inspect.getcallargs(backend.authenticate, request, **credentials)
        except TypeError:
            continue
        flag, user = backend.authenticate(request, **credentials)
        if not flag:
            user_login_failed.send(sender=__name__, credentials=_clean_credentials(credentials), request=request)
            return flag, user
        user.backend = backend_path
        return flag, user


