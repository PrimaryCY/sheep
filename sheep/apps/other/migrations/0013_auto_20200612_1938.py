# Generated by Django 2.2.7 on 2020-06-12 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0012_auto_20200612_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadhistorymodel',
            name='url',
            field=models.FileField(upload_to='', verbose_name='上传地址'),
        ),
    ]
