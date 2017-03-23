"""Production settings"""

from .default import *
from . import celery

DB_PATH = os.path.join(ROOT_DIR, 'sapoche_dev.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)

"""Celery setting module"""
CELERY = celery
