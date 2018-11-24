from flask import *
from flask_s3 import FlaskS3

from app_musicUploader.config import Config
from flask_login import LoginManager
from flask_cors import CORS
import boto3
import os

app_musicUploader = Flask(__name__)
CORS(app_musicUploader, origins=['https://musicuploader.damonqingsongmeng.com'])
app_musicUploader.config.from_object(Config)
login = LoginManager(app_musicUploader)

# Global variales
ROOT = os.path.dirname(os.path.abspath('imageUploader.py'))
IMAGE_FOLDER = '/tmp/images'
THUMBNAIL_FOLDER = '/tmp/thumbnails'
MUSIC_FOLDER = '/tmp/musics'
IMAGE_BUCKET_PREFIX = 'ece1779-images-'
THUMBNAIL_BUCKET_PREFIX = 'ece1779-thumbnails-'
MUSIC_BUCKET_PREFIX = 'ece1779-musics-'

# AWS services
s3_resource = boto3.resource('s3', **config.AWS_CONNECTION_ARGS)
s3_client = boto3.client('s3', **config.AWS_CONNECTION_ARGS)
dynamodb_resource = boto3.resource('dynamodb', **config.AWS_CONNECTION_ARGS)

from app_musicUploader import routes
