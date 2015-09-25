from celery import Celery

from .sqlalchemy import db  # noqa

celery = Celery('squash.tasks')
