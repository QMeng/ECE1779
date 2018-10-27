from flask import *
from flask_sqlalchemy import *
from app_worker.config import Config
from flask_login import LoginManager
import boto3

app_worker = Flask(__name__)
app_worker.config.from_object(Config)
db = SQLAlchemy(app_worker)
login = LoginManager(app_worker)
ROOT = os.path.dirname(os.path.abspath('imageUploader.py'))
IMAGE_FOLDER = os.path.join(ROOT, 'images')
THUMBNAIL_FOLDER = os.path.join(ROOT, 'thumbnails')
s3 = boto3.resource('s3', **config.AWS_CONNECTION_ARGS)
IMAGE_BUCKET_PREFIX = 'ece1779-images-'
THUMBNAIL_BUCKET_PREFIX = 'ece1779-thumbnails-'

from app_worker import routes
