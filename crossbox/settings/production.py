import os
from ._base import *  # noqa: F401, F403
from distutils.util import strtobool

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')
DEBUG = strtobool(os.getenv('DJANGO_DEBUG', 'False'))
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(',')
STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
]

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
