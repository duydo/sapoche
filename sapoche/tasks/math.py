from . import celery

__author__ = 'duydo'


@celery.task
def add(x, y):
    return x + y
