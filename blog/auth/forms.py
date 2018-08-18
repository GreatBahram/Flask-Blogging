# third-part imports
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

# local imports
from blog.models.user import UserModel


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        email = UserModel.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email is already in use.')

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me signed in')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = UserModel.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is not account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
