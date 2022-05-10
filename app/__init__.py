# from ensurepip import bootstrap
# from ensurepip import bootstrap
from flask_bootstrap import Bootstrap
from flask import Flask
from config import DevConfig
from config import config_options
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail



mail = Mail()
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    #intializing application
    app = Flask(__name__, instance_relative_config = True, static_url_path='/app/static/')

    #setting up configurations
    app.config.from_object(DevConfig)

    #creating the app configurations 
    app.config.from_object(config_options[config_name])

    #intializing flask extensions 
    mail.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix="/")


    #registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app