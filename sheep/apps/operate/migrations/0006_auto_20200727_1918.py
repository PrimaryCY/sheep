# Generated by Django 2.2.14 on 2020-07-27 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operate', '0005_auto_20200726_1806'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collectcategory',
            options={'ordering': ('-created_time',), 'verbose_name': '用户收藏帖子类别表', 'verbose_name_plural': '用户收藏帖子类别表'},
        ),
        migrations.AddField(
            model_name='collectcategory',
            name='total',
            field=models.PositiveIntegerField(default=0, verbose_name='总数'),
        ),
        migrations.AddField(
            model_name='praise',
            name='praise_or_trample',
            field=models.SmallIntegerField(default=0, verbose_name='赞或踩'),
        ),
    ]
