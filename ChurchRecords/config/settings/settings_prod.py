from .base_settings import *



SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-3ijz%tjd)vrqs9%z1nefr^i@sgprp9p&mp7f&$yt-we*@ig-p3')

DEBUG = 'RENDER' not in os.environ

DEBUG = True


RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)



DATABASES = {
    'default': dj_database_url.config(
        # Feel free to alter this value to suit your needs.
        default='postgresql://postgres:postgres@localhost:5432/mysite',
        conn_max_age=600
    )
}


STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
# if not DEBUG:
#     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
#     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
