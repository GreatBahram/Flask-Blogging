# app/__init__.py

import os
import secrets

# third-party imports
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# local imports
from blog.config import app_config

# variables initialization
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

# login_manger variable initialization
login_manager = LoginManager()
login_manager.login_view = 'auth.login_page'
login_manager.login_message_category = 'info'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import and register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    return app
