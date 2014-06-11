# -*- coding: utf-8 -*-
import os.path
import logging
from settings import *


SITE_SRC_ROOT = os.path.dirname(__file__)


DEBUG = True
TEMPLATE_DEBUG = DEBUG


LEVEL = logging.ERROR
if DEBUG:
    LEVEL = logging.DEBUG


LOG_FILENAME = 'debug.privilege.log'
logging.basicConfig(
    filename=os.path.join(SITE_SRC_ROOT, LOG_FILENAME),
    level=LEVEL,
    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django-privilege'
    }

#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'Your DB name',
#        'USER': 'Your DB account',
#        'PASSWORD': 'Your password',
#        'HOST': 'Your DB host',
#        'PORT': 'Your DB port',
#        'DATABASE_CHARSET': 'UTF8',
#    }
}


#INTERNAL_IPS = ('127.0.0.1',)
#DEBUG_TOOLBAR_PANELS = (
#    'debug_toolbar.panels.version.VersionDebugPanel',
#    
#    #'debug_toolbar.panels.timer.TimerDebugPanel',
#    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#    'debug_toolbar.panels.headers.HeaderDebugPanel',
#    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#    'debug_toolbar.panels.template.TemplateDebugPanel',
#    'debug_toolbar.panels.sql.SQLDebugPanel',
#    'debug_toolbar.panels.cache.CacheDebugPanel',
#    'debug_toolbar.panels.signals.SignalDebugPanel',
#    'debug_toolbar.panels.logger.LoggingPanel',
#)
