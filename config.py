class Config:
    """
    Common configurations
    Put any configurations here that are common across all environments
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
