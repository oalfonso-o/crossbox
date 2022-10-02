import os
from ._base import *  # noqa: F403, F401
from ._base import LOGGING
from distutils.util import strtobool

DEBUG = strtobool(os.getenv('DJANGO_DEBUG', 'True'))
LOCAL = strtobool(os.getenv('DJANGO_LOCAL', 'False'))
ALLOWED_HOSTS = ['*']

LOGGING['loggers'] = {
    'django': {
        'handlers': ['stdout'],
        'level': 'INFO',
    },
}
