# from django.test import TestCase

# Create your tests here.

# from django.dispatch import receiver

# import os

# os.popen('shutdown -h now')
#
# os.popen()

import qrcode
import json
from io import BytesIO
from PIL import Image
import base64
a =  {
    'a':1
}
img = qrcode.make(json.dumps(a))

io = BytesIO()

img.save(io)

image = Image.open(io)
# print(io.read())
print(base64.b64encode(io.read()))
# image.show()



