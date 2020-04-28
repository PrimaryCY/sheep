# Generated by Django 2.2.7 on 2019-12-03 18:39

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='状态')),
                ('name', models.CharField(max_length=128, verbose_name='帖子分类')),
                ('desc', models.CharField(max_length=512, null=True, verbose_name='分类简介')),
                ('author', models.IntegerField(db_index=True, verbose_name='创建人')),
                ('image', models.URLField(null=True, verbose_name='分类ICON')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='状态')),
                ('name', models.CharField(max_length=128, verbose_name='帖子名称')),
                ('author', models.IntegerField(db_index=True, verbose_name='创建人')),
                ('category', models.IntegerField(db_index=True, default=1, verbose_name='帖子分类')),
                ('desc', models.CharField(max_length=512, null=True, verbose_name='帖子简介')),
                ('content', models.TextField(verbose_name='帖子内容')),
                ('image', models.URLField(null=True, verbose_name='帖子icon')),
                ('post_num', models.IntegerField(default=0, verbose_name='评论数量')),
                ('read_num', models.IntegerField(default=0, verbose_name='阅读数量')),
                ('like_num', models.IntegerField(default=0, verbose_name='点赞数量')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
            },
        ),
    ]