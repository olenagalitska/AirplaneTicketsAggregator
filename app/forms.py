from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email

from app.models import Users


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class SearchForm(FlaskForm):
    departure = SelectField('FROM')
    arrival = SelectField('TO')
    date = DateField('DATE')


def validate_username(username):
    user = Users.query.filter_by(username=username).first()
    if user is not None:
        raise ValidationError("Please use a different username.")


def validate_email(email):
    user = Users.query.filter_by(email=email).first()
    if user is not None:
        raise ValidationError("Such email is already in use.")
