import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheep.settings')
django.setup()
from django.test import TestCase
from django.conf import settings
# Create your tests here.

