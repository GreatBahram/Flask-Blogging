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
from config import app_config

# db variable initialization
db = SQLAlchemy()
bcrypt = Bcrypt()

# login_manger variable initialization
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    # mail configuration
    app.config['MAIL_SERVER'] = 'smtp.yandex.com'
    app.config['MAIL_PORT'] = '465'
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

    # import and register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    mail = Mail(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login_page'
    login_manager.login_message_category = 'info'

    db.init_app(app)
    bcrypt.init_app(app)

    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('errors/401.html', title='Unauthorized'), 401

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    return app
