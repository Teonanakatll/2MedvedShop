DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db2',
        'USER': 'django_shop2',
        'PASSWORD': 'django_shop_db',
        'HOST': 'localhost',
        'PORT': '',
    }
}