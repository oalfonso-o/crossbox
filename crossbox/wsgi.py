"""
WSGI config for crossbox project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'crossbox.settings.production')

path = '/home/oalfonso/oalfonso.pythonanywhere.com'
if path not in sys.path:
    sys.path.insert(0, path)

application = get_wsgi_application()
