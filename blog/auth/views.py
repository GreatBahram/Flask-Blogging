import os
import secrets

# third-party imports
from flask import (abort, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required, login_user, logout_user

# local imports
from blog import bcrypt, db
from blog.auth import auth
from blog.auth.forms import (LoginForm, RegistrationForm, RequestResetForm,
                            ResetPasswordForm, UpdateAccountForm)
from blog.auth.utils import resent_email, save_picture
from blog.models.user import UserModel


@auth.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.login_page'))
    return render_template('auth/register.html', title="Sign Up", form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_url = request.args.get('next')
            return redirect(next_url) if next_url else redirect(url_for('home.homepage'))

        flash("Login unsuccessful. Please check your email and password", 'danger')
    return render_template('auth/login.html', title="Login", form=form)

@auth.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('home.homepage'))

@auth.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('auth.user_info'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('auth/account.html', title='Account',
            image_file=image_file, form=form)

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        resent_email(user)
        flash('An email has been sent with instruction to reset your password.', 'info')
        return redirect(url_for('auth.login_page'))

    return render_template('auth/reset_request.html', title='Reset Password', form=form)

@auth.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    user = UserModel.verify_reset_token(token)
    if user is None:
        flash('That is an invalid token or expired token.', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        pwdhash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = pwdhash
        # save user to the database
        db.session.commit()

        flash("Your password has been updated", 'success')
        return redirect(url_for('auth.login_page'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)

