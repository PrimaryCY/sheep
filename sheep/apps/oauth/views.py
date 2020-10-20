from django.contrib.auth import get_user_model
from django.db.transaction import on_commit
from django.db import transaction
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.conf import settings
from rest_framework.viewsets import GenericViewSet

from apps.oauth.models import Application, UserOAuth
from apps.user.tasks import after_login, after_user_create
from apps.oauth.serializer import ListApplicationSerializer, ListUserOauthSerializer
from apps.user.token import Token
from sheep.constant import RET
from utils.drf_extensions.decorators import only_data_cache_response
from utils.viewsets import ExtensionViewMixin

User = get_user_model()


class ApplicationViewSet(ExtensionViewMixin,
                         ListModelMixin,
                         GenericViewSet):
    """第三方应用视图"""
    serializer_class = {
        'list': ListApplicationSerializer
    }
    queryset = Application.objects.all()
    permission_classes = ()

    # 缓存30分钟
    # @only_data_cache_response(timeout=60 * 30)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OauthTokenView(APIView):
    """oauth自动登录视图"""
    permission_classes = ()

    @staticmethod
    def post(request, *args, **kwargs):
        code = request.data.get('code')
        app_name = request.data.get('app_name')

        if not all([code, app_name]):
            raise ValidationError({'code': RET.PARAMERR, 'msg': ''})

        try:
            app: Application = Application.objects.get(app_name=app_name)
        except Exception:
            raise ValidationError({'code': RET.PARAMERR, 'msg': '不支持该app'})

        info = app.app_modules.get_user_info(code)
        if not info:
            raise ValidationError({'code': RET.UNKOWNERR, 'msg': '未知错误，请重试'})

        user_oauth = UserOAuth.objects.filter(uid=info['id'], app=app).first()

        if user_oauth:
            # 有用户记录
            payload = User.generate_token_data(user_oauth.user)
            after_login.delay(user_oauth.user.id, request.u_host)
            data = {
                'token': Token.encryptTk(settings.TOKEN,
                                         request,
                                         payload),
                'type': 1
            }
            return Response(data=data)
        else:
            # 无用户记录,给用户一个随机值
            key = UserOAuth.save_app_user_info(info, app.id)
            if key is False:
                raise ValidationError({'code': RET.DBERR, 'msg': '数据库错误，请重试'})
            data = {
                'k': key,
                'app_name': app.app_name,
                'type': 2
            }
            return Response(data=data)


class OauthRegisterView(APIView):
    """oauth绑定已有用户或注册新用户视图"""
    permission_classes = ()

    @staticmethod
    def post(request, *args, **kwargs):
        t = request.data.get('t')
        # redis中存储第三方用户信息的key
        k = request.data.get('k')
        if not all([t, k]):
            raise ValidationError({'code': RET.PARAMERR, 'msg': ''})

        if t == 1 and request.user.is_anonymity:
            raise ValidationError({'code': RET.PARAMERR, 'msg': '未登录'})

        app_id, info = UserOAuth.get_app_user_info(k)
        if not info:
            raise ValidationError({'code': RET.PARAMERR, 'msg': '请重试！'})

        if t == 1:
            # oauth关联当前登录用户
            UserOAuth.objects.create(app_id=app_id,
                                     home_url=info['home_url'],
                                     user=request.user,
                                     uid=info['id'],
                                     extra_data=info)
            return Response(data='ok')
        else:
            # oauth自动注册新用户
            with transaction.atomic():
                user = User.objects.create(username=info['username'],
                                           portrait=info['portrait'],
                                           is_anonymity=False,
                                           is_active=True)
                UserOAuth.objects.create(app_id=app_id,
                                         user=user,
                                         uid=info['id'],
                                         extra_data=info,
                                         home_url=info['home_url'], )
                on_commit(lambda: after_user_create.delay(user.id))
                payload = User.generate_token_data(user)
                after_login.delay(user.id, request.u_host)

            data = {
                'token': Token.encryptTk(settings.TOKEN,
                                         request,
                                         payload),
            }
            return Response(data=data)


class UserOauth(ExtensionViewMixin,
                ListModelMixin,
                GenericViewSet):
    queryset = Application.objects.all()
    serializer_class = {
        'list': ListUserOauthSerializer
    }
