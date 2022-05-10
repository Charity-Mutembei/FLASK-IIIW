from distutils.debug import DEBUG
import os

class Config:
    '''
    General configuration parent class
    '''

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '53ce661657be0571ddac1f49'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://charity:naturelove@localhost/morgan'

    #email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    pass



class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}