# app/__init__.py

# third-party imports
from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

# login_manger variable initialization
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    # Circular problem
    from app.models import UserModel
    from app.forms import LoginForm, RegistrationForm

    bcrypt = Bcrypt(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login_page'
    login_manager.login_message_category = 'info'

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
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))

        form = RegistrationForm()
        if form.validate_on_submit():
            pwdhash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = UserModel(
                    username=form.username.data,
                    email=form.email.data,
                    password=pwdhash,)

            # save user to the database
            user.save_to_db()

            flash(f"Account created for {form.username.data}", 'success')
            return redirect(url_for('login_page'))
        return render_template('register.html', title="Sign Up", form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))

        form = LoginForm()
        if form.validate_on_submit():
            user = UserModel.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_url = request.args.get('next')
                return redirect(next_url) if next_url else redirect(url_for('home_page'))

            flash("Login unsuccessful. Please check your email and password", 'danger')
        return render_template('login.html', title="Login", form=form)

    @app.route('/logout')
    def logout_page():
        logout_user()
        return redirect(url_for('home_page'))

    @app.route('/account')
    @login_required
    def user_info():
        return render_template('account.html', title="User Info")

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
