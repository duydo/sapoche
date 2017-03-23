from celery import Celery

__author__ = 'duydo'


class FlaskCelery(object):
    """Flask Celery Extension"""

    _celery = None
    _app = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        _celery = Celery(__name__)
        _celery.config_from_object(app.config.get('CELERY'))

        Task = _celery.Task

        class ContextTask(Task):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return super(ContextTask, self).__call__(*args, **kwargs)

        _celery.Task = ContextTask
        self._celery = _celery
        self._app = app

    @property
    def app(self):
        return self._app

    @property
    def celery(self):
        if self._app is None:
            raise ValueError('The flask-celery extension has not been initialized.')
        return self._celery
