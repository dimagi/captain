import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '***'

DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangobower',
    'djcelery',
    'apps.deploy',
    'django_rq',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'chief.urls'
FILEPATH = os.path.abspath(os.path.dirname(__file__))
DJANGO_LOG_FILE = "%s/%s" % (FILEPATH, "captain.django.log")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'chief.wsgi.application'

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chief',
        'USER': 'chief',
        'PASSWORD': 'chief',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

BROKER_URL = 'redis://localhost:6379/0'

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'components')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

BOWER_INSTALLED_APPS = (
    'jquery#1.11.1',
    'underscore#1.6.0',
    'bootstrap#3.3.5',
    'knockout#3.3.0',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': DJANGO_LOG_FILE,
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 20  # Backup 200 MB of logs
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'NOTSET',
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'ERROR'
        },
        "rq.worker": {
            "handlers": ['console', "file"],
            "level": "DEBUG"
        },
    }
}

from chief_settings import *

try:
    from localsettings import *
except ImportError:
   raise
