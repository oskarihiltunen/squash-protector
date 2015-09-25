# -*- coding: utf-8 -*-
"""
    audi.settings.production
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains application settings specific to a production
    environment running on Heroku.
"""

import os

from .base import *  # noqa

#
# Generic
# -------

# If a secret key is set, cryptographic components can use this to sign cookies
# and other things. Set this to a complex random value when you want to use the
# secure cookie for instance.
SECRET_KEY = os.environ['SECRET_KEY']

# The debug flag. Set this to True to enable debugging of the application. In
# debug mode the debugger will kick in when an unhandled exception ocurrs and
# the integrated server will automatically reload the application if changes in
# the code are detected.
DEBUG = 'DEBUG' in os.environ

SERVER_NAME = os.environ['SERVER_NAME']
DOMAIN = SERVER_NAME

#
# Celery
# ------

REDIS_URL = os.environ['REDISCLOUD_URL']
BROKER_URL = REDIS_URL

#
# SQLAlchemy
# ----------

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
