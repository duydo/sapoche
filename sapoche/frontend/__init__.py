from .. import factory

__author__ = 'duydo'


def create_app(settings=None):
    app = factory.create_app(__name__, __path__)
    app.config.from_object(settings)
    return app
