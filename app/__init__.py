from flask import Flask,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_login import LoginManager

pagedown=PageDown()
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
login_manager=LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return None
login_manager.login_view = "auth.login"

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app