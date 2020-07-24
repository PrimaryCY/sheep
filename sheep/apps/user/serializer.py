# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/11/26 19:07
from datetime import date

from django.contrib.auth import get_user_model
from django.core.validators import URLValidator

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from apps.user.token import Token
from sheep import settings
from utils.exceptions import CodeError
from utils.extra_fields import RangeField
from utils.re_compile import ReCompile
from apps.user.authentication import authenticate
from sheep.constant import RET, error_map

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(label='邮箱或者手机号', write_only=True)
    password = serializers.CharField(label='密码', write_only=True)
    # code = serializers.CharField(label='验证码', write_only=True, required=False)
    user = serializers.ReadOnlyField()
    token = serializers.ReadOnlyField()

    @property
    def username_field(self):
        try:
            # self.model = get_user_model()
            username_field = get_user_model().E
        except:
            username_field = 'username'
        return username_field

    def validate(self, attrs):
        user_input = {
            self.username_field: attrs.get('email_or_phone'),
            'password': attrs.get('password'),
        }

        if not all({user_input.get(self.username_field),
                    user_input.get('password')}):
            raise serializers.ValidationError({'code': RET.LOGINERR, 'msg': '请输入用户名和密码'})
        flag, user = authenticate(self.context['request'], **user_input)

        if not flag:
            raise serializers.ValidationError({'code': RET.LOGINERR, 'msg': user})

        payload = User.generate_token_data(user)
        return {
            'token': Token.encryptTk(settings.TOKEN,
                                     self.context['request'],
                                     payload),
            'username': user.username,
        }

    @staticmethod
    def delete(request):
        """退出登录"""
        access = Token.deleteTk(settings.TOKEN, request, request.user.user_info)
        if not access:
            raise serializers.ValidationError({'code': RET.SERVERERR, 'msg': '未知错误'})


class ListCreateUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_email = serializers.ReadOnlyField(label='是否邮箱验证')
    is_phone = serializers.ReadOnlyField(label='是否手机验证')
    is_admin = serializers.ReadOnlyField(label='是否超管')
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='密码')
    last_login = serializers.DateTimeField(read_only=True, label='最后登录时间')
    last_login_province = serializers.CharField(read_only=True, label='最后登录地点-省份')
    last_login_city = serializers.CharField(read_only=True, label='最后登录地点-城市')

    login_num = serializers.ReadOnlyField(label='登录次数')
    phone = serializers.ReadOnlyField(label='手机号')
    gender = serializers.ReadOnlyField(label='性别')
    birth = serializers.ReadOnlyField(label='生日')
    brief = serializers.ReadOnlyField(label='简介')
    portrait = serializers.ReadOnlyField(label='头像')

    username = serializers.CharField(validators=[
        UniqueValidator(
                queryset=User.objects.filter(is_anonymity=False),
                message={'code':RET.PARAMERR, 'msg':'用户名已经注册!'}
            )], label='用户名')
    email = serializers.CharField(validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message={'code':RET.PARAMERR, 'msg':'邮箱已经注册!'}
        )])

    def validate_username(self, username):
        if ReCompile.Ipv4.match(username):
            raise CodeError(code=RET.PARAMERR, msg='用户名不符合规范')
        if ReCompile.SpecialStr.search(username):
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '用户名带有特殊字符!'})
        return username

    def validate_email(self,email):
        if ReCompile.SpecialStr.match(email):
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '邮箱不符合规则!'})
        return email

    def validate(self, attrs):
        attrs = User.set_default(attrs)
        return attrs

    class Meta:
        model = User
        exclude = ('created_time', 'update_time', 'is_active', 'is_anonymity')


class UpdateUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_email = serializers.ReadOnlyField(label='是否邮箱验证')
    is_phone = serializers.ReadOnlyField(label='是否手机验证')
    is_admin = serializers.ReadOnlyField(label='是否超管')
    last_login = serializers.DateTimeField(read_only=True, label='最后登录时间')
    login_num = serializers.ReadOnlyField(label='登录次数')
    last_login_province = serializers.CharField(read_only=True, label='最后登录地点-省份')
    last_login_city = serializers.CharField(read_only=True, label='最后登录地点-城市')
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    phone = serializers.CharField(validators=[
        UniqueValidator(
            queryset=User.objects.filter(is_anonymity=False,is_phone=True),
            message={'code': RET.PARAMERR, 'msg': '手机号已被注册!'}
        )],
        label='手机号',
        allow_null=True,
        required=False,)
    gender = RangeField(iterable=list(dict(User.gender_choices)),
                        label='性别',
                        required=False,
                        error_messages='性别传递错误!',
                        data_type=int
                        )
    portrait = serializers.CharField(validators=[
        # django原生的validators传入dict无效  只能传入str
        URLValidator(message='头像地址不正确!')
        ], label='头像', required=False)

    birth = serializers.DateField(label='生日',
                                  required=False,
                                  allow_null=True)

    def validate_phone(self, phone):
        if not phone:
            return phone
        if not ReCompile.Phone.match(phone):
            raise serializers.ValidationError({'code':RET.PARAMERR, 'msg': '手机号格式不正确'})
        return phone

    def validate_birth(self, birth):
        if not birth:
            return birth
        if birth > date.today():
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '生日填写不正确!'})
        return birth

    class Meta:
        model = User
        exclude = ListCreateUserSerializer.Meta.exclude+('password',)


class DeleteUserSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='密码')
    is_del = serializers.ChoiceField(choices=['y', 'n'], label='是否注销')

    def validated_password(self, password):
        if not self.instance.check_password(password):
            raise serializers.ValidationError('密码错误!')
        return password

    def validated_is_del(self, is_del):
        if is_del == 'n':
            raise serializers.ValidationError('注销失败!')
        return is_del

    @staticmethod
    def delete(user):
        user.is_active = False
        user.save()


class AllUserSerializer(serializers.ModelSerializer):
    """所有用户基本信息"""
    
    class Meta:
        model = User
        exclude = ('created_time', 'update_time', 'is_active', 'is_anonymity', 'password')
