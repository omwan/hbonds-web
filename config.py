class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    UPLOAD_FOLDER = "/app/moe/uploads"


class DevelopmentConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = "/Users/olivia/Documents/moe"
