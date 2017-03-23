import importlib
import pkgutil
import flask

from .middleware import HTTPMethodOverrideMiddleware
from .core import db, migrate, cache
from .settings import default as default_settings

__author__ = 'duydo'


def create_app(package_name=None, package_path=None, settings=None):
    """Create a :class:`Flask` application instance configured with common functionality for the Sapoche platform.
    :param package_name: the package name
    :param package_path: the package path
    :param settings: the setting object or module
    :return: Flask instance
    """
    app = flask.Flask(package_name, instance_relative_config=True)
    app.config.from_object(default_settings)
    app.config.from_object(settings)
    register_core_extensions(app)
    register_blueprints(app, package_name, package_path)
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
    return app


def register_core_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    cache.init_app(app)


def register_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.

    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, flask.Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv
