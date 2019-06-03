class BaseConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    protocol = 'postgresql://postgres:'
    password = 'Kinsman.'
    host = '@localhost'
    dbase = '/farmapi'
    SQLALCHEMY_DATABASE_URI = protocol+password+host+dbase


class ProductionConfig(BaseConfig):
    DEBUG = False
