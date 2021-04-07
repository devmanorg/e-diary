import os

from environs import Env

env = Env()
env.read_env()

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])

SECRET_KEY = env.str('SECRET_KEY', 'REPLACE_ME')

DEBUG = env.bool('DEBUG', True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('DATABASE_NAME', 'schoolbase.sqlite3'),
    }
}

INSTALLED_APPS = ['datacenter']

ROOT_URLCONF = 'project.urls'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
    },
]

USE_L10N = True

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_TZ = True
