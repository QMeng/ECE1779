from flask import *
from flask_sqlalchemy import *
from app.config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
ROOT = os.path.dirname(os.path.abspath('imageUploader.py'))
IMAGE_FOLDER = os.path.join(ROOT, 'images')
THUMBNAIL_FOLDER = os.path.join(ROOT, 'thumbnails')

from app import routes
