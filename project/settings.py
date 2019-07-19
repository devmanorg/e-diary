import os

from dotenv import load_dotenv
load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv("DATABASE_NAME", "schoolbase.sqlite3"),
    }
}

INSTALLED_APPS = ['datacenter']

SECRET_KEY = os.getenv("SECRET_KEY", "REPLACE_ME")

DEBUG = os.getenv("DEBUG", "true").lower() in ['yes', '1', 'true']

ROOT_URLCONF = "project.urls"

ALLOWED_HOSTS = ['*']


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
