# -*- coding: utf-8 -*-

from .base import *


# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
SECRET_KEY = ''


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = False


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# HOSTS CONFIGURATION
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = ['winstein.com.br']
