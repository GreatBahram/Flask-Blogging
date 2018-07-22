# third-part imports
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import (BooleanField, PasswordField, StringField,
                     SubmitField)


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    remember_me = BooleanField('Keep me signed in')
    submit = SubmitField('Login')
