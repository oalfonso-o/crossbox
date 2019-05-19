import os
from ._base import *  # noqa: F403, F401
from ._base import LOGGING
from distutils.util import strtobool

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')
DEBUG = strtobool(os.getenv('DJANGO_DEBUG', 'True'))
LOCAL = strtobool(os.getenv('DJANGO_LOCAL', 'False'))
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWD'),
    }
}

LOGGING['loggers']['']['handlers'] = ['stdout']
LOGGING['loggers']['crossbox']['level'] = 'DEBUG'
