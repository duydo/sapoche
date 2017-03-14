from celery import Celery

__author__ = 'duydo'


def create_celery_app():
    celery = Celery(__name__)
    register_tasks(celery)
    return celery


def register_tasks(celery):
    celery.autodiscover_tasks(['sapoche.tasks.fb'])
