# -*- coding: utf-8 -*-
"""
    audi.settings.base
    ~~~~~~~~~~~~~~~~~~

    This module contains global application settings that are common to all
    environments.
"""
import os

#
# Paths
# -----

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)

#
# Celery
# ------

CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['customjson']
CELERY_INCLUDE = ['squash.tasks']
CELERY_TASK_SERIALIZER = 'customjson'

#
# GitHub
# ------

GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
