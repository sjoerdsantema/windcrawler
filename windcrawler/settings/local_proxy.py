import os

# all base settings for Django
from .base import *

HOME_PAGE_MSG = "This is local proxy"
print("using local proxy")
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "local",
        'USER': "dblocaluser",
        "PASSWORD": "0KDwK614MKwrr5PF",
        "HOST": "127.0.0.1",
        "PORT": 6543,
    }
}