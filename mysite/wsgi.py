"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
from dj_static import Cling, MediaCling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = Cling(MediaCling(get_wsgi_application()))
application = DjangoWhiteNoise(application)
