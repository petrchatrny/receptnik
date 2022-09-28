import os


class MissingEnvironVariableError(Exception):
    pass


class BaseConfig(object):
    ALLOWED_MIMETYPES = ["image/jpeg", "image/png", "image/gif"]

    # email account setup
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # cloud for images
    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")


class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    API_KEY_LIMIT = 5

    # file uploading
    MAX_CONTENT_LENGTH = 1 * 1000 * 1000  # 1 MB

    # mail
    MAIL_DEBUG = False

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    SECRET_KEY = "krtecek"
    API_KEY_LIMIT = 10

    # file uploading
    MAX_CONTENT_LENGTH = 5 * 1000 * 1000  # 5 MB

    # mail
    MAIL_DEBUG = True

    # database setup
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
