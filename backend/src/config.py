
class DevelopmentConfig(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = ""
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/gtl_dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(object):
    DEBUG = False
    DEVELOPMENT = False
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False