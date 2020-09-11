import os

# all base settings for Django
from .base import *

#ALLOWED_HOSTS = ['windcrawler-3kmq3mj2cq-ez.a.run.app']
ALLOWED_HOSTS = ['*']
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY", "%+vb^r@2oxw*su666bnqv9f81x!j@bj@m@a44h!d*!s-jw1a14")

print("using production")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'root')
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
]

DB_USER_UN = os.environ.get("DB_USER_UN", "")
DB_USER_PW = os.environ.get("DB_USER_PW", 'abc')
DB_NAME = os.environ.get("DB_NAME", "production")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER_UN ,
        "PASSWORD": DB_USER_PW,
        "HOST": "/cloudsql/infinite-aura-289015:europe-west4:windcrawler"
    }
}