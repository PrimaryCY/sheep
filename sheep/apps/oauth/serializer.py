# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/10/13 09:59
from rest_framework import serializers

from apps.oauth.models import Application, UserOAuth


class ListApplicationSerializer(serializers.ModelSerializer):
    login_url = serializers.URLField(read_only=True, label='跳转链接')

    class Meta:
        model = Application
        fields = ('id', 'app_name', 'image', 'login_url', 'help_text', 'client_id')
