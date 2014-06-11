# -*- coding: utf-8 -*-
import os
import sys


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path = [parent_dir] + sys.path


ADMINS = (

)
MANAGERS = ADMINS


TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh.CN'

USE_I18N = True
USE_L10N = True
USE_TZ = False


ROOT_URLCONF = "urls"

MEDIA_ROOT = ''
MEDIA_URL = '/media/'


STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATE_DIRS = (
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.markup",
    "django.contrib.formtools",
    'django.contrib.admin',

    "privilege",
#    'debug_toolbar',
    "example",
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


SECRET_KEY = 'r-cc8mi-q63m@t1j&amp;s7^j@+lmw!90c*axck-14n2wc*_3#_&amp;8p'
SITE_ID = 1

#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
WSGI_APPLICATION = 'wsgi.application'
