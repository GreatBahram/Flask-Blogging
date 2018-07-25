# app/__init__.py

import os
import secrets

# third-party imports
from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from PIL import Image

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

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

    # Circular problem
    from app.models import UserModel

    # import and register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from app.forms import (LoginForm, RegistrationForm, RequestResetForm,
                           ResetPasswordForm, UpdateAccountForm)

    mail = Mail(app)
    bcrypt = Bcrypt(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login_page'
    login_manager.login_message_category = 'info'

    db.init_app(app)

    @app.route('/register', methods=['GET', 'POST'])
    def register_page():
        if current_user.is_authenticated:
            return redirect(url_for('home.homepage'))

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
            return redirect(url_for('home.homepage'))

        form = LoginForm()
        if form.validate_on_submit():
            user = UserModel.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_url = request.args.get('next')
                return redirect(next_url) if next_url else redirect(url_for('home.homepage'))

            flash("Login unsuccessful. Please check your email and password", 'danger')
        return render_template('login.html', title="Login", form=form)

    @app.route('/logout')
    def logout_page():
        logout_user()
        return redirect(url_for('home.homepage'))

    def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        f_name, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
        print(picture_path)

        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn

    @app.route("/account", methods=['GET', 'POST'])
    @login_required
    def user_info():
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('user_info'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
        return render_template('account.html', title='Account',
                image_file=image_file, form=form)

    def resent_email(user):
        token = user.get_reset_token()
        msg = Message(
                'Password Reset Request',
                sender='johni.mcafee@yandex.com',
                recipients=[user.email])
        msg.body = f"""To reset your password visit the following link:
{url_for('reset_token', token=token, _external=True)}
"""
        mail.send(msg)

    @app.route('/reset_password', methods=['GET', 'POST'])
    def reset_request():
        if current_user.is_authenticated:
            return redirect(url_for('home.homepage'))
        form = RequestResetForm()
        if form.validate_on_submit():
            user = UserModel.query.filter_by(email=form.email.data).first()
            resent_email(user)
            flash('An email has been sent with instruction to reset your password.', 'info')
            return redirect(url_for('login_page'))

        return render_template('reset_request.html', title='Reset Password', form=form)

    @app.route('/reset_password/<token>', methods=['POST', 'GET'])
    def reset_token(token):
        if current_user.is_authenticated:
            return redirect(url_for('home.homepage'))
        user = UserModel.verify_reset_token(token)
        if user is None:
            flash('That is an invalid token or expired token.', 'warning')
            return redirect(url_for('reset_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            pwdhash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = pwdhash
            # save user to the database
            db.session.commit()

            flash("Your password has been updated", 'success')
            return redirect(url_for('login_page'))
        return render_template('reset_token.html', title='Reset Password', form=form)


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
