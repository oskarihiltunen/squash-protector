# -*- coding: utf-8 -*-
"""
    audi.settings.base
    ~~~~~~~~~~~~~~~~~~

    This module contains global application settings that are common to all
    environments.
"""
import os
from datetime import timedelta

#
# Paths
# -----

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)

#
# Celery
# ------

PING_TASK_FREQUENCY = timedelta(seconds=int(os.environ.get('PING_TASK_FREQUENCY', '60')))

CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['customjson']
CELERY_INCLUDE = ['squash.tasks']
CELERY_TASK_SERIALIZER = 'customjson'
CELERYBEAT_SCHEDULE = {
    'keep_database_connection_alive': {
        'task': 'squash.tasks.keep_database_connection_alive',
        'schedule': PING_TASK_FREQUENCY,
    },
}

#
# GitHub
# ------

GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
