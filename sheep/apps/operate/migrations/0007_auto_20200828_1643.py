# Generated by Django 2.2.14 on 2020-08-28 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operate', '0006_auto_20200727_1918'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collect',
            options={'ordering': ('-created_time',), 'verbose_name': '用户收藏资源详情表', 'verbose_name_plural': '用户收藏资源详情表'},
        ),
    ]