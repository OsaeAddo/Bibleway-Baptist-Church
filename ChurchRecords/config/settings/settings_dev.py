from ChurchRecords.config.settings.settings_prod import SECRET_KEY
from .base_settings import *


SECRET_KEY = 'django-insecure-3ijz%tjd)vrqs9%z1nefr^i@sgprp9p&mp7f&$yt-we*@ig-p3'
ALLOWED_HOSTS = []

DEBUG = True




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

SMS_BACKEND = 'sms.backends.console.SmsBackend'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]