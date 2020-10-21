# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/12/17 18:28
import base64
import hashlib

from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.utils.crypto import constant_time_compare


class SHA256(PBKDF2PasswordHasher):
    """
    自定义密码验证类需要实现3个方法
    encode()初次设置密码时使用的
    verify()校验输入的密码是否正确
    must_update()是否需要更新
    """
    algorithm = "sha256"
    # iterations = 120000
    digest = hashlib.sha256

    def encode(self, password, *args, **kwargs):
        """
        加密方法
        :param password:原始密码
        :args salt: 盐
        :args iterations:迭代次数
        :return: 加密好的字符串
        """
        # assert salt and '$' not in salt
        # 传了迭代次数就用传入的迭代次数,没有就用默认的
        # iterations = iterations or self.iterations
        assert password is not None
        # 如果是修改个人信息而没有修改密码,直接返回密码
        if len(password) == 95 and '$' in password:
            return password
        # 如果前端已经加密密码了,就直接返回
        elif len(password) == 88:
            return '$'.join([self.algorithm, password])

        # 返回一个bytes类型数据
        hash = self._encode(password, digest=self.digest).encode()
        # 用base64解成ascii码
        hash = base64.b64encode(hash).decode('ascii').strip()
        return f"{self.algorithm}${hash}"

    def _encode(self, password, digest):
        digest = digest()
        digest.update(password.encode())
        return digest.hexdigest()

    def verify(self, password, encoded):
        """
        *******************************************************************
        被checkpassword调用,
        验证密码是否正确
        *******************************************************************
        :param password:前端传入的密码
        :param encoded: 数据库中保存的密码
        :return:
        """
        # 密码包含四个东西,密码加密算法名称,迭代次数,盐,hash
        algorithm, hash = encoded.split('$', 1)
        # 首先判断数据库密码和加密类是否同种加密
        assert algorithm == self.algorithm
        # 前面密码如果已经加密了就直接判断和数据库密码是否相等
        encoded_2 = self.encode(password)
        return constant_time_compare(encoded, encoded_2)

    def must_update(self, encoded):
        # algorithm, iterations, salt, hash = encoded.split('$', 3)
        # return int(iterations) != self.iterations
        return False
