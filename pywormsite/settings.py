# coding:utf-8
import os
import os.path
import yaml


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 上级目录
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# 本地目录
#path = os.path.dirname(__file__)


SECRET_KEY = 'brxs6fk)uu#f==x*tec9jk8-$-h7fv9gy@%(@v&^ksru34ra4g'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

TEMPLATE_DEBUG = False

# create database pywormsite default charset=utf8;

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'purus',
    'blog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pywormsite.my_middleware.IPMiddleware',
)

ROOT_URLCONF = 'pywormsite.urls'

WSGI_APPLICATION = 'pywormsite.wsgi.application'


def config():
    return yaml.load(
        open(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/config.yaml', 'r',
             encoding='utf8'))


config = config()
password = config["mysql"]["password"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pywormsite',
        'USER': 'root',
        'PASSWORD': password,
        'HOST': '',
        'PORT': '3306',
    }
}

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = ('static',)

STATIC_ROOT = os.path.join(BASE_DIR, 'pywormsite/static')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

DEFAULT_CHARSET = 'utf-8'

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = [
#     '.pyworm.com',
# ]

#缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache',  #python manage.py createcachetable django_cache
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000  #最大条目数
        }
    }
}

#日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s-%(levelname)s: %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{0}/logs/request.txt'.format(path),
            'formatter': 'standard',
        },
        'error_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{0}/logs/error.txt'.format(path),
            'formatter': 'standard',
        },
        'chat_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{0}/logs/chat.txt'.format(path),
            'formatter': 'standard',
        },
        'access_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{0}/logs/access.txt'.format(path),
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'request': {
            'handlers': ['request_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'error': {
            'handlers': ['error_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'chat': {
            'handlers': ['chat_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'access': {
            'handlers': ['access_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

