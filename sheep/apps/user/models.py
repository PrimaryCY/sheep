import datetime
from collections import defaultdict
from typing import Union, Iterable

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import Sum, Count
from django.conf import settings
from django.forms import model_to_dict

from sheep.init_server import init_stdout
from utils.django_util.models import BaseModel
from utils.tools import rounding


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
    last_login_province = models.CharField(max_length=12, verbose_name='上次登录省份', null=False, default='')
    last_login_city = models.CharField(max_length=24, verbose_name='上次登录城市', null=False, default='')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    @property
    def website_age(self):
        """
        网站年龄
        :return:
        """
        result = datetime.datetime.now() - self.created_time
        return rounding(str(result.days/365))

    @property
    def age(self):
        """
        实际年龄
        :return:
        """
        if not self.birth:
            return '保密'
        return datetime.date.today().year - self.birth.year

    # 用户默认数据
    defautl_man_portrait = 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2519824424,1132423651&fm=26&gp=0.jpg'
    defautl_women_portrait = 'https://dss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=283284588,2796778480&fm=26&gp=0.jpg'

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
        user = cls.objects.filter(id=user_id).values('id', 'username', 'portrait').first()
        return dict(user) if user else {'username': "用户未找到"}

    @classmethod
    def bulk_get_simple_user_info(cls, ids: Iterable):
        """
        批量获取简单用户信息
        :param ids:
        :return:
        """
        return_dict = defaultdict(lambda :{'username': "用户未找到"})
        for i in cls.objects.filter(id__in=ids).values('id', 'username', 'portrait'):
            return_dict[i['id']] = i
        return return_dict

    @classmethod
    def get_simple_users_info(cls, *args):
        """
        批量获取简单通用用户信息
        :param args:
        :return:{1:{username:xxx,portrait:xxx}}
        """
        args = list(set(*args))
        users = cls.objects.filter(id__in=args).values('id', 'username', 'portrait')
        return {item['id']: item for item in users}

    @classmethod
    def generate_anonymity_user(cls, username):
        """
        创建匿名用户
        :param username:
        :return:
        """
        user, flag = cls.objects.get_or_create(defaults={'portrait': cls.defautl_man_portrait,},
                                               username=username,
                                               is_anonymity=True,
                                               is_active=True)
        return user, flag

    @classmethod
    def get_post_retrieve_author_info(cls, user_id: Union[int, object]):
        """
        获取文章作者信息
        :param user_id:
        :return:
        """
        from apps.post.models import Post

        if isinstance(user_id, User):
            user = user_id
        else:
            user = User.objects.filter(id=user_id).only('id', 'portrait', 'username', 'created_time', 'birth', 'is_active').first()
            if not user:
                return {}
        res = model_to_dict(user, fields=('id', 'portrait', 'username', 'created_time', 'birth', 'is_active'))
        res['age'] = user.age
        res['website_age'] = user.website_age
        post_aggregate = Post.objects.filter(author_id=user.id).aggregate(Sum('praise_num'), Sum('like_num'))
        res['article_total'] = Post.objects.filter(author_id=user.id, post_type=1).only('id').count()
        res['praise_total'] = post_aggregate['praise_num__sum']
        res['like_total'] = post_aggregate['like_num__sum']
        return res

    @classmethod
    @init_stdout('super user')
    def create_default_super_user(cls):
        assert settings.ADMIN_PHONE, (
            "settings.ADMIN_PHONE必须有内容！详情请看sheep.local_setting_example.py文件."
        )

        for i, p in enumerate(settings.ADMIN_PHONE):
            defaults = {
                'username': f'admin-{i}',
                'password': '123456',
                'phone': p
            }
            defaults = cls.set_default(defaults)
            cls.objects.get_or_create(phone=p, is_phone=True, defaults=defaults)
