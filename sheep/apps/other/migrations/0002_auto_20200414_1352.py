# Generated by Django 2.2.7 on 2020-04-14 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadhistorymodel',
            name='url',
            field=models.FileField(upload_to='', verbose_name='上传地址'),
        ),
    ]
