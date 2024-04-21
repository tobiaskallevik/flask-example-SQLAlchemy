# Contains the configuration for the flask app
# Different configurations are used for different environments

class Config(object):
    SECRET_KEY = "fdsafasd"
    UPLOAD_FOLDER = "image_pool"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ENV = 'production'


class DevelopmentConfig(Config):
    DATABASE_URI = 'sqlite:///database_files/flask.db'


class StagingConfig(Config):
    DATABASE_URI = 'postgresql://postgres:Zanto123@localhost/flask'


class ProductionConfig(Config):
    DATABASE_URI = 'postgresql://postgres:Zanto123@localhost/flask'
