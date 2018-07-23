# third-part imports
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)
# local imports
from app.models import UserModel

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
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    remember_me = BooleanField('Keep me signed in')
    submit = SubmitField('Login')
