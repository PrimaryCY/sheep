# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/8/26 17:16
import asyncio

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = '这只是一个测试命令'

    def add_arguments(self, parser):
        """
        自定义命令
        :param parser:
        :return:
        """
        parser.add_argument('poll_ids', nargs='+', type=str)

    async def _handle(self, id):
        await asyncio.sleep(3)
        self.stdout.write(id)

    def handle(self, *args, **options):
        print(options)
        tasks = [self._handle(i) for i in options['poll_ids']]
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        for poll_id in options['poll_ids']:
            ...

            # raise CommandError('Poll "%s" does not exist' % poll_id)

        self.stdout.write(self.style.SUCCESS(f'执行完成 {options["poll_ids"]}'))
