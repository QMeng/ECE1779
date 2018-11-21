from flask import *
from app_musicUploader.config import Config
from flask_login import LoginManager
import boto3
import os

app_musicUploader = Flask(__name__)
app_musicUploader.config.from_object(Config)
login = LoginManager(app_musicUploader)

# Global variales
ROOT = os.path.dirname(os.path.abspath('imageUploader.py'))
IMAGE_FOLDER = os.path.join(ROOT, 'images')
THUMBNAIL_FOLDER = os.path.join(ROOT, 'thumbnails')

# AWS services
s3_resource = boto3.resource('s3', **config.AWS_CONNECTION_ARGS)
s3_client = boto3.client('s3', **config.AWS_CONNECTION_ARGS)
dynamodb_resource = boto3.resource('dynamodb', **config.AWS_CONNECTION_ARGS)
IMAGE_BUCKET_PREFIX = 'ece1779-images-'
THUMBNAIL_BUCKET_PREFIX = 'ece1779-thumbnails-'

from app_musicUploader import routes
