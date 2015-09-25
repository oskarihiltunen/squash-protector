from celery import Celery
from flask.ext.github import GitHub

from .kombu import register_kombu_custom_serializer
from .sqlalchemy import db  # noqa

register_kombu_custom_serializer()
celery = Celery('squash.tasks')
github = GitHub()
