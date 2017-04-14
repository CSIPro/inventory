import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inventory',
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PW'),
        'HOST': 'localhost',
        'PORT': '',
    }
}
