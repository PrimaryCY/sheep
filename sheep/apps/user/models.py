import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from sheep import settings
from utils.models import BaseModel


# 用户.
class User(BaseModel, AbstractBaseUser):
    gender_choices = (
        (0, '女'),
        (1, '男'),
        (2, '保密')
    )
    username = models.CharField(max_length=50, verbose_name='用户名', unique=True)
    phone = models.CharField(max_length=11, null=True, verbose_name='手机号码', db_index=True)
    email = models.EmailField(max_length=100, verbose_name='邮箱', db_index=True)
    is_email = models.BooleanField(default=False, verbose_name='邮箱认证')
    gender = models.SmallIntegerField(choices=gender_choices, default=2, verbose_name='性别')
    portrait = models.URLField(null=True, blank=True, verbose_name='头像')
    is_phone = models.BooleanField(default=False, verbose_name='手机认证')
    birth = models.DateField(default=None, null=True, verbose_name='生日')
    is_admin = models.BooleanField(default=False, verbose_name='角色')
    is_anonymity = models.BooleanField(default=False, verbose_name='匿名')
    login_num = models.IntegerField(default=0, verbose_name='登录次数')
    brief = models.CharField(max_length=200, verbose_name='个人简介', null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    # 用户默认数据
    defautl_man_portrait = '123'
    defautl_women_portrait = '321'

    class Meta:
        verbose_name_plural = verbose_name = '用户表'
        unique_together = ('username', 'is_active',)

    @classmethod
    def set_default(cls, attrs):
        """
        设置用户默认数据
        :return:
        """
        phone = attrs.get('phone')
        # 当手机号在超管范围内,给予超管权限
        if phone in settings.ADMIN_PHONE:
            attrs['is_admin'] = True

        # 设置默认头像
        portrait = attrs.get('portrait')
        gender = attrs.get('gender')
        if not portrait:
            attrs['portrait'] = cls.defautl_women_portrait if gender == 2 else cls.defautl_man_portrait

        return attrs

    def __str__(self):
        return self.username if self.username else self.phone

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.password.startswith('pbkdf2_sha256$150000$'):
            self.set_password(self.password)
        super().save(force_insert, force_update, using, update_fields)

    def after_login(self):
        """
        用户成功登录后的操作
        :return:
        """
        self.login_num += 1
        self.last_login = datetime.datetime.now()
        self.save()
        return self

    @staticmethod
    def generate_token_data(user) -> dict:
        """
        返回token的加密数据
        :param user: 
        :return: dict
        """
        return {
            'id': user.id,
            'username': user.username
        }

    @classmethod
    def get_simple_user_info(cls, user_id: int):
        """
        获取简单通用用户信息
        :param user_id:
        :return:
        """
        return dict(cls.objects.filter(id=user_id).values('id', 'username').first())
