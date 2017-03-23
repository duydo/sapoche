import importlib
import inspect
import pkgutil

from flask_restful import Api, Resource

from .. import factory

__author__ = 'duydo'

api = Api()


def create_app(settings=None):
    app = factory.create_app(__name__, __path__)
    app.config.from_object(settings)
    print register_restful_api_resources(app)
    return app


def register_restful_api_resources(app):
    resources = []
    for _, name, _ in pkgutil.iter_modules(__path__):
        module_name = '%s.%s' % (__name__, name)
        m = importlib.import_module(module_name)
        for item in dir(m):
            item = getattr(m, item)
            if inspect.isclass(item) and issubclass(item, Resource):
                resources.append(item)
    api.init_app(app)
    return resources
