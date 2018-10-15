from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email

from app.models import User


class LoginForm(FlaskForm):
    '''User login form, this form is used in login page'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit1 = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    '''Sign up form, this form is used in sign up page'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit2 = SubmitField('Sign Up')

    def validate_username(self, username):
        '''this method validates the inputted username is meeting the standard'''
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        '''this method validates the inputted user email is meeting the standard'''
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class FileForm(FlaskForm):
    '''File form, this form is used in upload page'''
    file = FileField('image', validators=[FileRequired(),
                                          FileAllowed(['jpg', 'jpeg', 'png', 'tiff', 'exif', 'gif'], 'Images only!')])
