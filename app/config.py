import os


class BaseConfig:
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    PROJECT_NAME = 'NLine'
    PROJECT_URL = os.environ.get('PROJECT_URL') or 'https://inlinev1.herokuapp.com'
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTHY_API_KEY = os.environ['AUTHY_API_KEY']
    GOOGLE_CREDENTIALS = os.environ['GOOGLE_CREDENTIALS']
    GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    stripe_secret_key = os.environ['stripe_secret_key']
    stripe_publishable_key = os.environ['stripe_publishable_key']
