from django.db import models

from utils.models import BaseModel
# Create your models here.


class UploadHistoryModel(BaseModel):
    user_id = models.IntegerField(verbose_name='创建人', null=False)
    url = models.FileField(verbose_name='上传地址', null=False)

    def __str__(self):
        return f'{self.user_id}:{self.url}'

    class Meta:
        verbose_name_plural = verbose_name = '上传文件历史表'
        ordering = ('-created_time',)
