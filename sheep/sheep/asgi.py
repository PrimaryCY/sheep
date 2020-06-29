# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/11/15 11:13
import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheep.settings')
django.setup()
application = get_default_application()

# from sheep.init_server import server

# server.init()


