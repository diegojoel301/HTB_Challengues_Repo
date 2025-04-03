from application.util import generate

class Config(object):
    SECRET_KEY = generate(50)
    UPLOAD_FOLDER = '/app/application/static/screenshots'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True