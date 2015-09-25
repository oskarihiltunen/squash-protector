# -*- coding: utf-8 -*-
"""
    squash-protector
    ~~~~~~~~~~~~~~~~

    This module contains the Flask application core.
"""
import importlib
import os
import pkgutil
import warnings

from flask import Flask, jsonify
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.contrib.fixers import ProxyFix

from .extensions import celery, db

warnings.simplefilter('error', SAWarning)


class Application(Flask):
    def __init__(self, environment=None):
        super(Application, self).__init__(__name__)
        self._init_settings(environment)
        self._init_extensions()
        self._init_errorhandlers()
        self._init_views()
        self._init_after_request_handlers()
        self.wsgi_app = ProxyFix(self.wsgi_app, num_proxies=2)

    def _init_settings(self, environment=None):
        """
        Initialize application configuration.

        This method loads the configuration from the given environment
        (production, development, test).  If no environment is given as an
        argument, the environment is read from ``FLASK_ENV`` environmental
        variable.  If ``FLASK_ENV`` is not defined, the environment defaults to
        development.

        The environment specific configuration is loaded from the module
        corresponding to the environment in :module:`.settings`.

        :param environment: the application environment
        """
        if environment is None:
            environment = os.environ.get('FLASK_ENV', 'development')
        settings_module = 'squash.settings.' + environment
        self.config.from_object(settings_module)

    def _init_extensions(self):
        """Initialize and configure Flask extensions with this application."""
        celery.config_from_object(self.config)
        db.init_app(self)

    def _init_views(self):
        pass

    def _init_errorhandlers(self):
        @self.errorhandler(400)
        def bad_request(error):
            return jsonify(title='Bad request.'), 400

        @self.errorhandler(404)
        @self.errorhandler(NoResultFound)
        def object_not_found(error):
            return jsonify(title='Not found.'), 404

        @self.errorhandler(405)
        def method_not_allowed(error):
            return jsonify(
                title='The method is not allowed for the requested URL.'
            ), 405

        @self.errorhandler(500)
        def internal_error(error):
            return jsonify(title='Internal server error.'), 500

    def _init_after_request_handlers(self):
        @self.after_request
        def prevent_caching(response):
            response.cache_control.no_cache = True
            return response


def load_models():
    """
    Load models from the subpackages of the application.

    This is implemented by iterating over the subpackages of the
    application and trying to import `models` module/package under the
    subpackage.
    """

    allowed_folders = [
        __name__
    ]

    for loader, name, is_package in pkgutil.iter_modules(allowed_folders):
        if is_package:
            module_path = loader.path.replace('/', '.')
            try:
                importlib.import_module(
                    name='.'.join([module_path, name, 'models']),
                    package=__name__
                )
            except ImportError:
                pass
