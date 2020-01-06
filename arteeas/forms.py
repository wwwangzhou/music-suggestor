from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from arteeas.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # check if the newly registered user is alreay in the database
    def validate_username(self, username):
        user_existed = User.query.filter_by(username=username.data).first()
        if user_existed:
            raise ValidationError('That username is taken. Please choose a different one.') # part of wtform

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) # just make sure to skip empty music
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class MusicForm(FlaskForm):
    title = StringField('Author', validators=[DataRequired()])
    content = TextAreaField('Title', validators=[DataRequired()])
    submit = SubmitField('Music')
