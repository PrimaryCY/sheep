# -*- coding: utf-8 -*-
# author:CY
# datetime:2020/8/26 17:16
import time
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import wait

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

    def thread_handle(self, id):
        time.sleep(3)
        self.stdout.write(id)

    def handle(self, *args, **options):

        start_time = time.time()

        pool = ThreadPoolExecutor(10)
        # for i in pool.map(self.thread_handle, options['poll_ids']):
        #     print(i)

        tasks = [pool.submit(self.thread_handle, i) for i in options['poll_ids']]

        # # 循环最后的所有列表,如果出现异常就抛出
        for data in tasks:
            if data.exception():
                # 如果发生异常了,就将其它尚未执行的任务给取消掉
                for i in tasks:
                    i.cancel()
                return data.exception()

        pool.shutdown()

        for poll_id in options['poll_ids']:
            ...

            # raise CommandError('Poll "%s" does not exist' % poll_id)

        self.stdout.write(self.style.SUCCESS(f'执行完成 {options["poll_ids"]}'))
        self.stdout.write(f'{time.time()-start_time}')