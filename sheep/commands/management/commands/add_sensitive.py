# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/8/26 17:16
import time

from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic

from apps.post.models import Sensitive


class Command(BaseCommand):
    help = '添加敏感词'

    def add_arguments(self, parser):
        """
        自定义命令
        :param parser:
        :return:
        """
        parser.add_argument('keyword', nargs='+', type=str)

    def handle(self, *args, **options):
        start_time = time.time()
        with atomic():
            Sensitive.objects.bulk_create([Sensitive(key_word=i) for i in options['keyword']])
            Sensitive.delete_cache()

        self.stdout.write(self.style.SUCCESS(f'添加敏感词 {options["keyword"]} 成功！'))
        self.stdout.write(f'{time.time()-start_time}')
