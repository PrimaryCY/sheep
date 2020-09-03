# from django.test import TestCase

# Create your tests here.


from functools import partial


def xx(a, b):
    print(a,b)

xx2 = partial(xx, a=1)
xx2(13)