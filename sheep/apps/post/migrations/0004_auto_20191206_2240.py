# Generated by Django 2.2.7 on 2019-12-06 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_category_parent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='parent',
            new_name='parent_id',
        ),
    ]