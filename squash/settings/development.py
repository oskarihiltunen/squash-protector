# -*- coding: utf-8 -*-
"""
    audi.settings.development
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains application settings specific to a development
    environment.
"""

from .base import *  # flake8: noqa

#
# Generic
# -------

# If a secret key is set, cryptographic components can use this to sign cookies
# and other things. Set this to a complex random value when you want to use the
# secure cookie for instance.
SECRET_KEY = 'development key'

# The debug flag. Set this to True to enable debugging of the application. In
# debug mode the debugger will kick in when an unhandled exception ocurrs and
# the integrated server will automatically reload the application if changes in
# the code are detected.
DEBUG = True

SERVER_NAME = os.environ.get('SERVER_NAME', 'localhost:5000')


#
# Celery
# ------

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
BROKER_URL = REDIS_URL


#
# Database
# --------

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'postgres://localhost/squash-protector'
)
