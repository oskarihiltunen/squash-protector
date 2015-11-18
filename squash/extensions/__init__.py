from celery import Celery
from flask.ext.github import GitHub

from .kombu import register_kombu_custom_serializer
from .sqlalchemy import db  # noqa


class CustomGitHub(GitHub):

    def get_access_token(self):
        return None

    def request(
            self,
            method,
            resource,
            access_token='',
            all_pages=False,
            **kw):
        if not access_token:
            raise ValueError('access_token is required')
        auth = 'token %s' % access_token
        headers = kw.setdefault('headers', {})
        headers['Authorization'] = auth
        return GitHub.request(
            self,
            method,
            resource,
            all_pages=all_pages,
            **kw
        )

register_kombu_custom_serializer()
celery = Celery('squash.tasks')
github = CustomGitHub()
