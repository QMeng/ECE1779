from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model
from werkzeug.security import generate_password_hash, check_password_hash

from app_musicUploader import *
from app_musicUploader.config import *


class UserInfo(Model):
    '''
    User information table in dynamodb
    '''

    class Meta:
        '''
        Metadata for UserInfo table
        '''
        table_name = 'UserInfo'
        region = 'us-east-1'
        aws_access_key_id = AWS_CONNECTION_ARGS.get('aws_access_key_id')
        aws_secret_access_key = AWS_CONNECTION_ARGS.get('aws_secret_access_key')

    username = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute()
    password = UnicodeAttribute()

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        '''
        set the password (hashed with salt)
        '''
        self.password = generate_password_hash(password)

    def check_password(self, password):
        '''
        :return: true if the password is correct
        '''
        return check_password_hash(self.password, password)


class MusicInfo(Model):
    '''
    Music information table in dynamodb
    '''

    class Meta:
        '''
        Metadata for MusicInfo table
        '''
        table_name = 'MusicInfo'
        region = 'us-east-1'
        aws_access_key_id = AWS_CONNECTION_ARGS.get('aws_access_key_id')
        aws_secret_access_key = AWS_CONNECTION_ARGS.get('aws_secret_access_key')

    username = UnicodeAttribute(hash_key=True)
    musicname = UnicodeAttribute(range_key=True)
    imagename = UnicodeAttribute()
    s3MusicBucket = UnicodeAttribute()
    s3ImageBucket = UnicodeAttribute()
    s3ThumbnailBucket = UnicodeAttribute()

    def set_musicname(self, musicname):
        '''
        set the music name
        '''
        self.musicname = musicname
        return self

    def set_imagename(self, imagename):
        '''
        set the image name
        '''
        self.imagename = imagename
        return self

    def set_s3MusicBucket(self, s3MusicBucket):
        self.s3MusicBucket = s3MusicBucket
        return self

    def set_s3ImageBucket(self, s3ImageBucket):
        '''
        set the s3 image bucket attribute
        '''
        self.s3ImageBucket = s3ImageBucket
        return self

    def set_s3ThumbnailBucket(self, s3ThumbnailBucket):
        '''
        set the s3 thumbnail bucket attribute
        '''
        self.s3ThumbnailBucket = s3ThumbnailBucket
        return self


class MusicList(Model):
    '''
    Music list table
    '''

    class Meta:
        '''
        Metadata for MusicList table
        '''
        table_name = 'MusicList'
        region = 'us-east-1'
        aws_access_key_id = AWS_CONNECTION_ARGS.get('aws_access_key_id')
        aws_secret_access_key = AWS_CONNECTION_ARGS.get('aws_secret_access_key')

    username = UnicodeAttribute(hash_key=True)
    musicname = UnicodeAttribute(range_key=True)

    def set_musicname(self, musicname):
        '''
        set the music name
        '''
        self.musicname = musicname
        return self


class InvalidUsage(Exception):
    '''Exception class for error handling'''
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@login.user_loader
def load_user(username):
    '''load user
    '''
    return UserInfo.get(username)
