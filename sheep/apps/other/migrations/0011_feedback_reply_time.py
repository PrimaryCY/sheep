# Generated by Django 2.2.7 on 2020-06-11 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other', '0010_auto_20200604_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='reply_time',
            field=models.DateTimeField(null=True, verbose_name='回复时间'),
        ),
    ]
