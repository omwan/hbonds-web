import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class ProductionConfig(Config):
    UPLOAD_FOLDER = "/home/ssi/hbonds-web/moe/uploads"
    MOE_FOLDER = "/home/ssi/hbonds-web/moe"


class DevelopmentConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = "/Users/olivia/Documents/moe"
    MOE_FOLDER = "/Users/olivia/Documents/GitHub/hbonds-web/moe"
