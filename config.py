import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gWfMjs2uXjUd7EeG'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://psql_user:cUgjfhjMuVX4Ydvg@localhost:5432/whatafly'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ARANGO_SETTINGS = {'host': 'localhost', 'port': 8529}
    # ARANGO_DB = 'whataflyDB'

    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
