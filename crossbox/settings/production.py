import os
from ._base import *  # noqa: F401, F403
from distutils.util import strtobool

DEBUG = strtobool(os.getenv('DJANGO_DEBUG', 'False'))
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(',')
STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT')
