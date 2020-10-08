# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/26 23:50
from collections import Mapping

import msgpack
from cryptography.fernet import Fernet, InvalidToken
from typing import Union


class Token(object):

    """
    user_info = {
        'username': 1
    }
    user_info.get(key) 👇
    """
    key = 'username'
    # request中的ua属性映射,根据框架的选择有不同的mapping
    ua_map = {
        'django': 'META.HTTP_USER_AGENT',
        'flask': 'user_agent.platform'
    }

    def __init__(self, config: dict, request=None):
        """
        :param config:配置文件
                    example:
                        TOKEN = {
                            'FRAME': 'django'
                            'TOKEN_SECURITY_KEY': b'pBy0j5_m6qqTOXElHSs0OlfV5qiYhqHkEvwLtdrXZ5o=',
                            'TOKEN_EXPIRES': 7*24*3600, #redis的key过期时间
                            'TOKEN_REDIS': None,        #连接redis的实例
                            'TOKEN_UNIQUE': True,       #是否单端登录
                        }
        :param request:请求对象
        """
        assert config.get('TOKEN_SECURITY_KEY'), (
            'settings未设置TOKEN_SECURITY_KEY!'
        )
        assert config.get('FRAME'), (
            'settings未设置FRAME!'
        )
        self.security_key = config.get('TOKEN_SECURITY_KEY')
        self.frame = config.get('FRAME').lower()
        self.token_unique = config.get('TOKEN_UNIQUE', True)

        if config.get('TOKEN_REDIS'):
            # 设置token过期时间,默认七天
            self.expires = config.get('TOKEN_EXPIRES', 7*24*3600)
            self.redis = config.get('TOKEN_REDIS')

        self.conf = config

        self.request = request

    def get_ua(self):
        """
        获取ua字符串
        :return: str
        """
        iter = self.ua_map.get(self.frame).split('.')
        ua = self.request
        for i in iter:
            if isinstance(ua, Mapping):
                ua = ua.get(i, None)
                assert ua, (
                    f'{ua}并没有key:{i}'
                )
            elif isinstance(ua, object):
                ua = getattr(self.request, i)
        return ua or ''

    @property
    def redis_key(self):
        """获取redis中存入的key名,来控制可以几端登录"""
        if not hasattr(self, '_redis_key'):
            if self.token_unique:
                self._redis_key = f'tk_pc_{self.data.get(self.key)}'
            else:
                ua = self.get_ua()
                if 'android'in ua or 'Linux' in ua:
                    self._redis_key = f'tk_android_{self.data.get(self.key)}'
                elif 'iphone' in ua:
                    self._redis_key = f'tk_ios_{self.data.get(self.key)}'
                else:
                    self._redis_key = f'tk_pc_{self.data.get(self.key)}'
        return self._redis_key

    @property
    def token(self):
        """获得加密实例"""
        if not hasattr(self, '_token'):
            self._token = Fernet(self.security_key)
        return self._token

    def _generate_token(self) -> str:
        """生成token"""
        wait_token = msgpack.dumps(self.data)
        return (self.token.encrypt(wait_token)).decode()[::-1]

    def _encryptTk(self, data: Mapping) -> Union[str, bool]:
        """
        加密token
        """
        assert isinstance(data, Mapping), (
            "data必须是一个字典类型|类字典类型的数据"
        )

        self.data = dict(data)
        token = self._generate_token()
        if self.redis:
            assert data.get(self.key, None), (
                '传入的属性必须要有唯一标识属性ID来作为redis的key!')

            res = self.redis.setex(self.redis_key, self.expires, token)
            if not res:return False
        return token

    def _deleteTk(self, data: Mapping) -> bool:
        """删除token"""
        assert isinstance(data, Mapping), (
            "data必须是一个字典类型|类字典类型的数据"
        )

        if self.redis:
            assert data.get(self.key, None), (
                '传入的属性必须要有唯一标识属性ID来作为redis的key!')
            self.data = data
            return self.redis.delete(self.redis_key)

    def _unpackTk(self, token: str) -> Union[dict, bool]:
        """
        :return:dict
        """
        try:
            bytes_user_info = self.token.decrypt(token.encode()[::-1])
            user_info = msgpack.loads(bytes_user_info,encoding='utf8')
        except InvalidToken:
            return False
        except Exception as ex:
            raise ex

        if self.redis:
            self.data = user_info
            res = self.redis.get(self.redis_key)
            res = res.decode('utf8') if isinstance(res, bytes) else res
            if not res:
                return False
            elif res != token.replace(' ', ''):
                return False
        return user_info

    @classmethod
    def encryptTk(cls, config: dict, request: object, data: Mapping) -> Union[str, bool]:
        """
        加密接口
        :param config:配置文件,dict形式
        :param request:request的请求实例
        :param data: 类字典或者字典形式对象
        :return: 加密成功返回token,
                 加密失败返回false布尔值
        """
        return cls(config, request)._encryptTk(data)

    @classmethod
    def unpackTk(cls, config: dict, request: object, token: str) -> Union[dict, bool]:
        """
        解密接口
        :param config: 配置文件,dict形式
        :param request:request的请求实例
        :param token: token字符串
        :return: 解密成功返回user_info对象
                 解密失败返回false布尔值
        """
        return cls(config, request)._unpackTk(token)

    @classmethod
    def deleteTk(cls, config: dict, request: object, data: Mapping)->bool:
        """
        删除redis中token
        :param config:配置文件,dict形式
        :param request:request的请求实例
        :param data: 映射对象,主要是寻找redis-key使用
        :return: 布尔值
        """
        return cls(config, request)._deleteTk(data)
