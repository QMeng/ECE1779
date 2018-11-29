from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email

from app_musicUploader.models import UserInfo


class LoginForm(FlaskForm):
    '''User login form, this form is used in login page'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submitLoginInfo = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    '''Sign up form, this form is used in sign up page'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submitSignUpInfo = SubmitField('Sign Up')

    def validate_username(self, username):
        '''this method validates the inputted username is meeting the standard'''
        number = UserInfo.count(username.data)
        if number != 0:
            raise ValidationError('Please use a different username.')


class FileUploadForm(FlaskForm):
    '''File form, this form is used in upload page'''
    image = FileField('image', validators=[FileRequired(),
                                           FileAllowed(['jpg', 'jpeg', 'png', 'tiff', 'exif', 'gif'], 'Images only!')])
    music = FileField('music', validators=[FileRequired(),
                                          FileAllowed(['wav', 'aiff', 'mp3', 'aac', 'wma', 'flac', 'aac'], 'Musics only!')])
