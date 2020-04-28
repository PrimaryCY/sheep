# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/4/14 10:52
import os

from rest_framework import serializers
from django.conf import settings

from apps.other.models import UploadHistoryModel
from utils.extra_fields import CurrentUserIdDefault, RangeField
from utils.tools import random_filename


class UploadSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=CurrentUserIdDefault())
    url = serializers.FileField(read_only=True)

    file = serializers.FileField(required=True, label='文件', write_only=True)
    upload_path = RangeField(iterable=os.listdir(settings.MEDIA_ROOT),
                             label='上传目录',
                             required=False,
                             error_messages='不存在此目录!',
                             write_only=True)

    def validate(self, attrs):
        file = attrs.pop('file')
        upload_path = attrs.pop('upload_path', '')
        attrs['url'] = self.save_file(file, upload_path)
        return attrs

    @staticmethod
    def save_file(file, upload_path):
        """
        保存上传的文件
        :param file: 文件对象
        :param upload_path: 文件要保存的目录
        :return:
        """
        file.name = random_filename(file.name)
        file_path = os.path.join(settings.MEDIA_ROOT, upload_path, file.name)

        with open(file_path, 'wb') as f:
            for i in file.chunks():
                f.write(i)

        return os.path.join(upload_path, file.name)

    class Meta:
        model = UploadHistoryModel
        exclude = ('is_active',)
