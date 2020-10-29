import ast
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.utils.module_loading import import_string
from django_extensions.db.fields.json import JSONField
from django.utils.functional import cached_property
from django.conf import settings

from utils.django_util.models import BaseModel
from utils.tools import url_join_args

# Create your models here.

User = get_user_model()


class Application(BaseModel):
    id = models.BigAutoField(primary_key=True)
    app_name = models.CharField(max_length=255, verbose_name='应用名称')
    chinese_app_name = models.CharField(max_length=255, default='', verbose_name='应用中文名称')
    client_id = models.CharField(max_length=100, db_index=True)
    client_secret = models.CharField(max_length=255, db_index=True)
    image = models.URLField(verbose_name='图片icon')
    redirect_uri = models.URLField(verbose_name='回调uri', default='')
    scope = models.CharField(max_length=512, default='')
    load_modules = models.CharField(max_length=512, default='')
    help_text = models.CharField(max_length=64, default='', verbose_name='图片提示文字')

    @cached_property
    def app_modules(self):
        return import_string(self.load_modules)(self)

    @cached_property
    def login_url(self):
        return self.app_modules.login_url

    class Meta:
        verbose_name_plural = verbose_name = 'app'
        ordering = ('id',)

    def __str__(self):
        return self.load_modules


class UserOAuth(BaseModel):
    app = models.ForeignKey(Application, related_name='user_oauth',
                            on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='oauth', null=True,
                             on_delete=models.CASCADE)
    extra_data = JSONField(verbose_name='额外内容')
    uid = models.BigIntegerField(verbose_name='第三方用户id')
    home_url = models.URLField(verbose_name='用户个人首页', null=True)
    con = settings.OAUTH_REDIS

    # token = dangerous(settings, settings.ITSDANGEROUSTOKEN['EXPIRS'])

    # def encode_token(self, user):
    #     token = self.token.dumps(user.id)
    #     return token.decode('utf8')

    class Meta:
        verbose_name_plural = verbose_name = 'user_oauth'
        ordering = ('-created_time',)

    @classmethod
    def save_app_user_info(cls, info, app):
        """
        临时存储第三方网站的用户信息到redis
        :param info:
        :param app:
        :return:
        """
        #
        key = uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.uuid1().hex))
        flag = cls.con.set(str(key), str({
            'info': info,
            'app_info': model_to_dict(app),
        }), ex=10*60)
        if not flag:
            return False
        return key

    @classmethod
    def get_app_user_info(cls, key):
        data = cls.con.get(key)
        try:
            data = ast.literal_eval(data)
        except:
            cls.del_app_user_info(key)
            return None, None
        return data['app_info'], data['info']

    @classmethod
    def del_app_user_info(cls, key):
        return cls.con.delete(key)

    def __str__(self):
        return self.extra_data
