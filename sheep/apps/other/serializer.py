# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/4/14 10:52
import json
import os
import datetime
from urllib import parse

from django_celery_results.models import TaskResult
from qiniu import Auth, BucketManager
from rest_framework.request import Request
from rest_framework import serializers
from django.conf import settings

from apps.other.models import UploadHistoryModel, FeedbackCategory, Feedback
from apps.post.models import Category
from apps.post.serializer import PostCategorySerializer
from sheep.constant import RET
from utils.extra_fields import CurrentUserIdDefault, RangeField, SerializerMethodAndWriteField
from utils.tools import random_filename


class UploadTokenSerializer(serializers.Serializer):
    """七牛云token接口"""

    bucket = serializers.CharField(required=True, label='桶', write_only=True)

    tk = serializers.CharField(read_only=True, label='七牛token')

    def validate(self, attrs):
        q = Auth(**settings.QI_NIU_CLOUD['auth'])
        bucket = BucketManager(q)

        # buckets, _ = bucket.buckets()
        buckets = settings.QI_NIU_CLOUD['base_url'].keys()

        bucket = attrs.get('bucket')
        if bucket not in buckets:
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '桶不存在'})

        expires = settings.QI_NIU_CLOUD.get('expires')
        return {
            'tk': q.upload_token(bucket, expires=expires, policy=self.get_policy(bucket))
        }

    def get_policy(self, bucket):
        return {
            'returnBody': json.dumps({
                'success': True,
                'code': RET.OK,
                'data': {
                    'url': parse.urljoin(settings.QI_NIU_CLOUD['base_url'].get(bucket), '$(key)'),
                    'key': '$(key)',
                    'size': '$(fsize)'
                }
            })
        }


class UploadHistorySerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=CurrentUserIdDefault())
    url = serializers.URLField(label='资源链接')
    bucket = serializers.CharField(label='桶')
    file = serializers.CharField(label='资源名称')
    raw_file = serializers.CharField(label='资源原名')
    size = serializers.FloatField(label='大小')

    def validate_size(self, size):
        """文件大小,保留一位小数,以 kb 为单位"""
        size = size/1024
        return round(size, 1)

    # url = serializers.FileField(read_only=True)
    # file = serializers.FileField(required=True, label='文件', write_only=True)
    # upload_path = RangeField(iterable=os.listdir(settings.MEDIA_ROOT),
    #                          label='上传目录',
    #                          required=False,
    #                          error_messages='不存在此目录!',
    #                          write_only=True)

    def validate(self, attrs):
        # file = attrs.pop('file')
        # upload_path = attrs.pop('upload_path', '')
        # attrs['url'] = self.save_file(file, upload_path)
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


class OptionSerializer(serializers.Serializer):
    post_category = serializers.SerializerMethodField(label='帖子类别')

    def get_post_category(self, obj):
        return PostCategorySerializer(Category.objects.filter(level=0),
                                      many=True,
                                      context=self._context).data


class FeedbackCategorySerializer(serializers.ModelSerializer):
    """查看反馈类别"""
    author_id = serializers.HiddenField(default=CurrentUserIdDefault())

    class Meta:
        model = FeedbackCategory
        exclude = ("created_time", 'update_time', 'is_active')


class ListFeedbackSerializer(serializers.ModelSerializer):
    """查看反馈列表"""
    class Meta:
        model = Feedback
        fields = "__all__"


class CreateFeedbackSerializer(serializers.ModelSerializer):
    """提交反馈"""
    author_id = serializers.HiddenField(default=CurrentUserIdDefault(), label='创建人')
    category_id = serializers.IntegerField(label='类别')

    def validate_category_id(self, category_id):
        f_c = FeedbackCategory.objects.filter(id=category_id).only('id').first()
        if not f_c:
            raise serializers.ValidationError({'code': RET.PARAMERR, 'msg': '不存在此类别!'})
        return category_id

    class Meta:
        model = Feedback
        exclude = ('reply', 'reply_author_id', 'is_active')


class UpdateFeedbackSerializer(serializers.ModelSerializer):
    reply_author_id = serializers.HiddenField(default=CurrentUserIdDefault(), label='回复人id')
    reply_time = serializers.DateTimeField(read_only=True, label='回复时间')

    def validate(self, attrs):
        attrs['reply_time'] = datetime.datetime.now()
        return attrs

    class Meta:
        model = Feedback
        fields = ('reply_author_id', 'reply', 'reply_time')


class CeleryResultsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.context.get('view'):
            return
        view = self.context['view']
        if view.action == 'list':
            self.Meta.fields = ('id', 'task_id', 'status', 'date_created', 'date_done', 'task_name', 'worker')
        else:
            self.Meta.fields = '__all__'

    class Meta:
        model = TaskResult
        fields = "__all__"
