import os
basedir = os.path.abspath(os.path.dirname(__file__))

DBUSER = 'postgres'
DBPASS = ''
DBHOST = 'localhost'
DBPORT = 5432
DBNAME = 'foodmania'


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost:5432/foodmania'


class TestingConfig(Config):
    TESTING = True