import os
from flask import *
from flask_sqlalchemy import *
from app.config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


from app import routes