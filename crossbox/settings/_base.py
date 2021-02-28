import os
import sys
import stripe
from distutils.util import strtobool

from dotenv import find_dotenv, load_dotenv

from crossbox.constants import WEBHOOKS

ENVIRONMENT_FILE = os.getenv('DJANGO_ENV_FILE', find_dotenv())
load_dotenv(ENVIRONMENT_FILE)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ENVIRONMENT = os.getenv('DJANGO_PROJECT_ENVIRONMENT')

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_filters',
    'django_extensions',
    'rest_framework',
    'crossbox',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'crossbox.middleware.LoginRequiredMiddleware',
]

NOT_LOGIN_REQUIRED_ROUTES = [
    'login',
    'user-create',
    'password_reset',
    'password_reset_done',
    'password_reset_confirm',
    'password_reset_complete',
    *[webhook['route_name'] for webhook in WEBHOOKS],
]

ROOT_URLCONF = 'crossbox.urls'

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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa e501
        'OPTIONS': {
            'min_length': 4,
        }
    },
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'crossbox.wsgi.application'
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT', '')

CSRF_USE_SESSIONS = True
JET_DEFAULT_THEME = 'default'
JET_SIDE_MENU_COMPACT = True

LOGIN_URL = '/'
LOGIN_EXEMPT_URLS = ()
LOGIN_REDIRECT_URL = 'reservation/'
LOGOUT_REDIRECT_URL = LOGIN_URL

EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER', 'admin@localhost')
EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD', 'password')
EMAIL_PORT = os.getenv('DJANGO_EMAIL_PORT', '587')
EMAIL_USE_TLS = strtobool(os.getenv('DJANGO_EMAIL_USE_TLS', 'False'))
EMAIL_USE_SSL = strtobool(os.getenv('DJANGO_EMAIL_USE_SSL', 'False'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'syslog': {
            'format':
                f'{os.getenv("PROJECT_NAME")}: %(process)d '
                '- %(levelname)s:%(name)s:%(message)s',
        },
        'debug': {
            'format':
                '%(asctime)s.%(msecs)03d %(levelname)s '
                '[%(name)s:%(funcName)s #%(lineno)s] %(message)s',
            'datefmt': '%H:%M:%S',
         },
    },
    'handlers': {
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'syslog',
            'address': '/dev/log',
        },
        'stdout': {
            'formatter': 'debug',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['syslog', 'stdout'],
            'level': 'INFO',
        },
        'crossbox': {
            'handlers': ['syslog', 'stdout'],
            'level': 'DEBUG',
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

stripe.api_key = os.getenv('DJANGO_STRIPE_SECRET_KEY')

BASE_URL = os.getenv('DJANGO_BASE_URL')

SMTP_SERVER_NOTIFICATIONS = os.getenv('DJANGO_SMTP_SERVER_NOTIFICATIONS')
SMTP_PORT_NOTIFICATIONS = os.getenv('DJANGO_SMTP_PORT_NOTIFICATIONS')
SMTP_USER_NOTIFICATIONS = os.getenv('DJANGO_SMTP_USER_NOTIFICATIONS')
SMTP_PASSWORD_NOTIFICATIONS = os.getenv('DJANGO_SMTP_PASSWORD_NOTIFICATIONS')
SMTP_ADMIN_NOTIFICATIONS = os.getenv('DJANGO_SMTP_ADMIN_NOTIFICATIONS')
SMTP_BOSS_NOTIFICATIONS = os.getenv('DJANGO_SMTP_BOSS_NOTIFICATIONS')
