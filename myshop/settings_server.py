
DEBUG = False

ALLOWED_HOSTS =  ['3112.site']


STATIC_URL = 'https://static.3112.site/static/'
MEDIA_URL = 'https://static.3112.site/media/'

MEDIA_ROOT = '/home3/media_files'
STATIC_ROOT = '/home3/static_files'

# YANDEX_METRICA_COUNTER_ID = '90756370'


CSRF_TRUSTED_ORIGINS = ['http://3112.site', 'https://3112.site']

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'pass123..',
        'HOST': 'db_myshop',
        'PORT': '5432',
    }
    }
