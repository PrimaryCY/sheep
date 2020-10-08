# Generated by Django 2.2.14 on 2020-10-08 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='状态')),
                ('content', models.TextField(null=True, verbose_name='关于我们')),
            ],
            options={
                'verbose_name': '关于我们',
                'verbose_name_plural': '关于我们',
                'ordering': ('-created_time',),
            },
        ),
    ]
