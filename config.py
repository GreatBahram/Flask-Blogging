import os

class Config:
    """
    Common configurations
    Put any configurations here that are common across all environments
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'SMTP Address'
    MAIL_PORT = 'PORT'
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "FakeK3y"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

app_config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
        }
