import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    JSON_SORT_KEYS=False

    JWT_SECRET_KEY = os.environ.get("SECRET_KEY")
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.environ.get("DATABASE_URL")
        if not value:
            raise ValueError("DATABASE_URL is not set")
        return value
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING=True

environment = os.environ.get("FLASK_DEBUG")

if environment:
    app_config = DevelopmentConfig()
else:
    app_config = TestingConfig()
