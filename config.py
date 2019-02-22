import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class ProductionConfig(Config):
    UPLOAD_FOLDER = "/app/moe/uploads"


class DevelopmentConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = "/Users/olivia/Documents/moe"
