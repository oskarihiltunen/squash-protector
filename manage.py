#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import os
import uuid

from flask import current_app, url_for
from flask.ext.failsafe import failsafe
from flask.ext.script import Manager, Server

from management.database import manager as database_manager


@failsafe
def create_app():
    from squash import Application
    return Application()


manager = Manager(create_app)
manager.add_command('runserver', Server(host='localhost'))
manager.add_command('database', database_manager)


@manager.shell
def make_shell_context():
    from squash.extensions import db
    from squash import load_models

    load_models()
    context = {}
    context['app'] = current_app
    context['db'] = db
    context.update(db.Model._decl_class_registry)

    return context


@manager.command
def generate_secret_key():
    """Generate a good unique secret key."""
    print(base64.b64encode(os.urandom(40)))


@manager.command
def add_project(repo):
    """Add a project and create a webhook URL for it.

    Repo should be for in format 'owner/repository'."""
    from squash.extensions import db
    from squash.models import Project
    project = Project(id=uuid.uuid4(), repo=repo)
    db.session.add(project)
    db.session.commit()
    print(url_for('events.receive', project_id=project.id, _external=True))

if __name__ == '__main__':
    manager.run()
