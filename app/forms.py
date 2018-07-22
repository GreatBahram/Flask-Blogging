# third-part imports
from flask_wtf import FlaskForm
from flask_wtf.validators import DataRequired, Email, EqualTo, Length
from wtforms import (BooleanField, EmailField, PasswordField, StringField,
                     SubmitField)


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    remember_me = BooleanField('Keep me signed in')
    submit = SubmitField('Login')
