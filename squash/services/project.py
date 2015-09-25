import uuid

from flask import url_for

from squash.extensions import db, github
from squash.models import Project


def create(repo, token):
    """Add a project and create a webhook for it.

    Repo should be for in format 'owner/repository'."""
    project = Project(id=uuid.uuid4(), repo=repo, access_token=token)
    db.session.add(project)
    create_hook(project)
    return project


def create_hook(project):
    hook_url = url_for(
        'events.receive',
        project_id=project.id,
        _external=True,
    )
    response = github.post(
        'repos/{0.repo}/hooks'.format(project),
        access_token=project.access_token,
        data={
            'name': 'web',
            'config': {
                'url': hook_url,
                'content_type': 'json',
            },
            'events': 'pull_request',
            'active': True,
        },
    )
    return response
