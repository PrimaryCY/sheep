# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/10/13 17:06
import abc
import functools
import requests
from requests.exceptions import ConnectionError

requests.packages.urllib3.disable_warnings()

from django.utils.functional import cached_property
from requests import request, HTTPError

from apps.oauth.models import Application
from utils.tools import url_join_args


def http_error_decorator(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (HTTPError, ConnectionError, KeyError) as ex:
            return
    return wrap


class BaseApp(metaclass=abc.ABCMeta):
    APP_URL = None
    ACCESS_TOKEN_URL = None
    INFO_URL = None

    def __init__(self, m: Application):
        self._m = m
        self.client_id = self._m.client_id
        self.client_secret = self._m.client_secret
        self.scope = self._m.scope
        self.redirect_uri = self._m.redirect_uri

    @cached_property
    def login_url(self):
        """
        跳转链接
        :return:
        """
        # params = {}
        # if self.client_id:
        #     params['client_id'] = self.client_id
        # if self.scope:
        #     params['scope'] = self.scope
        # if self.redirect_uri:
        #     params['redirect_uri'] = self.redirect_uri
        # return url_join_args(self.APP_URL, **params)

        return url_join_args(self.APP_URL, client_id=self.client_id, scope=self.scope, redirect_uri=self.redirect_uri)

    @abc.abstractmethod
    def get_user_info(self, code):
        """
        返回第三方平台用户信息
        格式：
            {
                'id': 第三方平台id，
                'username': 用户名,
                'portrait': 用户头像,
                'home_url': 用户首页
            }
        :param code:
        :return:
        """
        ...


    def _request(self, url, method='GET', *args, **kwargs):
        kwargs['headers'] = {
            **{
                'Accept': "application/json"
            },
            **kwargs.get('headers', {})
        }
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('verify', False)

        response = request(method, url, *args, **kwargs)

        response.raise_for_status()
        return response

    def get_json(self, url, *args, **kwargs):
        return self._request(url, *args, **kwargs).json()


class GitHubApp(BaseApp):
    APP_URL = 'https://github.com/login/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    INFO_URL = 'https://api.github.com/user'

    def _get_access_token(self, code):
        json = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            # 'redirect_uri': self.redirect_uri
        }
        response = self.get_json(
            self.ACCESS_TOKEN_URL,
            method='POST',
            json=json
        )
        return response.get('access_token')

    def _get_user_info(self, access_token):
        response = self.get_json(self.INFO_URL, headers={
            'Authorization': f'token {access_token}'
        })
        response['portrait'] = response['avatar_url']
        response['username'] = f'{response["login"]}-github'
        response['home_url'] = response['html_url']
        return response

    @http_error_decorator
    def get_user_info(self, code):
        """
        返回第三方平台用户信息
        """
        access_token = self._get_access_token(code)
        if not access_token:
            return
        return self._get_user_info(access_token)


class WeiBoApp(BaseApp):
    APP_URL = 'https://api.weibo.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
    INFO_URL = 'https://api.weibo.com/2/users/show.json'

    def _get_access_token(self, code):
        json = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        response = self.get_json(
            self.ACCESS_TOKEN_URL,
            method='POST',
            params=json
        )
        return response

    def _get_user_info(self, tk_response):
        """
        返回第三方平台用户信息
        """
        params = {
            'access_token': tk_response.get('access_token'),
            'uid': tk_response.get('uid')
        }
        response = self.get_json(self.INFO_URL, params=params)
        response['portrait'] = response['avatar_large']
        response['username'] = f'{response["name"]}-weibo'
        response['home_url'] = f'https://www.weibo.com/{response["profile_url"]}'
        return response

    @http_error_decorator
    def get_user_info(self, code):
        response = self._get_access_token(code)
        if not response.get('access_token'):
            return
        return self._get_user_info(response)
