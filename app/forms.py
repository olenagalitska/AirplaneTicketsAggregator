from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


def validate_username(form, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
        raise ValidationError("Please use a different username.")


def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
        raise ValidationError("Such email is already in use.")


class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Password Repeat',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')


class SearchForm(FlaskForm):
    departure = SelectField('City A', validators=[DataRequired()])
    arrival = SelectField('City B', validators=[DataRequired()])
    date = DateField('Departure Date', validators=[DataRequired()])
    adults = IntegerField("Adults")
    teens = IntegerField("Teens")
    infants = IntegerField("Infants")
    children = IntegerField("Children")
    seniors = IntegerField("Seniors")
    wizzair = BooleanField("Wizzair")
    ryanair = BooleanField("Ryanair")
    uia = BooleanField("UIA")

    def validate_adults(adults):
        if adults < 0 or adults > 10:
            raise ValidationError("Please pick the number of adults from 0 to 10")

    def validate_teens(teens):
        if teens < 0 or teens > 10:
            raise ValidationError("Please pick the number of teens from 0 to 10")

    def validate_children(children):
        if children < 0 or children > 10:
            raise ValidationError("Please pick the number of children from 0 to 10")

    def validate_infants(infants):
        if infants < 0 or infants > 10:
            raise ValidationError("Please pick the number of infants from 0 to 10")

    def validate_seniors(seniors):
        if seniors < 0 or seniors > 10:
            raise ValidationError("Please pick the number of seniors from 0 to 10")
