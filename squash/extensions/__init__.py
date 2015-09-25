from celery import Celery
from flask.ext.github import GitHub

from .sqlalchemy import db  # noqa

celery = Celery('squash.tasks')
github = GitHub()
