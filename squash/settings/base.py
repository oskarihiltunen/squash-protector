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
CELERY_ACCEPT_CONTENT = ['json']
CELERY_INCLUDE = ['squash.tasks']
CELERY_TASK_SERIALIZER = 'json'
