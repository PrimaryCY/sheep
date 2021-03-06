# Generated by Django 2.2.14 on 2020-10-31 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operate', '0012_auto_20201029_1446'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdynamic',
            options={'ordering': ('-created_time__date',), 'verbose_name': '用户动态表', 'verbose_name_plural': '用户动态表'},
        ),
        migrations.RemoveField(
            model_name='userdynamic',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='praise',
            name='t',
            field=models.PositiveSmallIntegerField(choices=[(1, '文章'), (2, '评论')], db_index=True, verbose_name='资源类型'),
        ),
        migrations.AlterField(
            model_name='userdynamic',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间'),
        ),
    ]
