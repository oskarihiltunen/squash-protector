#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import os

from flask import current_app
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

if __name__ == '__main__':
    manager.run()
