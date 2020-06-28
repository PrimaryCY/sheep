from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "自定义命令"

    def handle(self, *args, **options):
        print('args', args)
        print('options', options)
        self.stdout.write('执行完毕')

