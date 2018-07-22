# app/__init__.py

# third-party imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config
from forms import LoginForm, RegistrationForm

# db variable initialization
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    @app.route('/')
    @app.route('/home')
    def home_page():
        return render_template('home.html', title="Welcome")

    @app.route('/about')
    def about_page():
        return render_template('about.html', title="About")

    @app.route('/register', methods=['GET', 'POST'])
    def register_page():
        form = RegistrationForm()
        return render_template('register.html', title="Sign Up", form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        form = LoginForm()
        return render_template('login.html', title="Login", form=form)

    @app.errorhandler(401)
    def forbidden(error):
        return render_template('errors/401.html', title='Forbidden'), 403

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
