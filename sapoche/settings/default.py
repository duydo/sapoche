"""Sapoche Default Settings"""

import os

DEBUG = False

"""Common settings"""

SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
APP_DIR = os.path.abspath(os.path.join(SETTINGS_DIR, os.pardir))
ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, os.pardir))

SECRET_KEY = os.environ.get('SAPOCHE_SECRET', 'FssAvXB9p43xAQsN6fvj7i3u1tjRDn8u')

# Cache
CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.

# SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
