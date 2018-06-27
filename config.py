from V1 import app


class BaseConfig(object):
    """Initializes"""
    app.DEBUG = True
    app.SECRET_KEY = 'cbbfvfjjfjjjfsjajjkkvsjh4636787531r9898298981'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    """initializes"""
    DEBUG = False
    TESTING = True
