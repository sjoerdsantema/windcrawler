import os

# all base settings for Django
from .base import *

print("using local proxy")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'root')
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
]

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