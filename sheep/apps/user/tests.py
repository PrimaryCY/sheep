from django.conf import settings

from rest_framework.test import APIClient, APITestCase

from apps.user.models import User

# from django.dispatch import receiver

# import os

# os.popen('shutdown -h now')
#
# os.popen()

# import qrcode
# import json
# from io import BytesIO
# from PIL import Image
# import base64
# a =  {
#     'a':1
# }
# img = qrcode.make(json.dumps(a))
#
# io = BytesIO()
#
# img.save(io)
#
# image = Image.open(io)
# # print(io.read())
# print(base64.b64encode(io.read()))
# # image.show()


TEST_USER_PHONE = '17635268011'


def setUpModule():
    print("setUpModule >>>")
    defaults = {
        'username': 'test',
        'password': '123456',
        'phone': TEST_USER_PHONE,
        'is_phone': True
    }
    User.objects.create(**defaults)

    settings.CELERY_ALWAYS_EAGER = True
    settings.BROKER_BACKEND = 'memory'


def tearDownModule():
    print("\ntearDownModule >>>")


class LoginTestCase(APITestCase):

    def test_post_login(self):
        response = self.client.post('/api/v1/web/login/', data={
            'email_or_phone': TEST_USER_PHONE,
            'password': '123456'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 2000)

    def test_post_error_login(self):
        response = self.client.post('/api/v1/web/login/', data={
            'email_or_phone': TEST_USER_PHONE,
            'password': '123456789'
        })
        self.assertEqual(response.json()['code'], 4102)

    def test_delete_login(self):
        user = User.objects.filter(phone=TEST_USER_PHONE).first()
        user.user_info = User.generate_token_data(user)
        self.client.force_authenticate(user)

        response = self.client.delete('/api/v1/web/login/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 2000)


class UserTestCase(APITestCase):

    def setUp(self):
        user = User.objects.filter(phone=TEST_USER_PHONE).first()
        user.user_info = User.generate_token_data(user)
        self.client.force_authenticate(user)
        super().setUpClass()

    def test_get_user(self):
        response = self.client.get('/api/v1/web/user/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 2000)
        self.assertEqual(response.json()['data']['phone'], TEST_USER_PHONE)

    def test_post_user(self):
        new_user_name = '测试账号'
        new_user_email = "907031022@qq.com"
        response = self.client.post('/api/v1/web/user/', data={
            'username': new_user_name,
            'email': new_user_email,
            'password': '123456',
        })

        self.assertEqual(response.status_code, 200)

        new_user = User.objects.filter(username=new_user_name, email=new_user_email).first()

        self.assertTrue(new_user)
        self.assertEqual(new_user.username, new_user_name)
        self.assertEqual(new_user.email, new_user_email)

    def test_put_user(self):
        response = self.client.put('/api/v1/web/user/', data={
            'password': '123456',
            'gender': 1,
            'birth': '2020-09-01',
            'portrait': 'http://www.baidu.com'
        })

        self.assertEqual(response.status_code, 200)

        user = User.objects.filter(phone=TEST_USER_PHONE).first()

        self.assertTrue(user)
        self.assertEqual(user.gender, 1)
        self.assertEqual(str(user.birth), '2020-09-01')
        self.assertEqual(user.portrait, 'http://www.baidu.com')
