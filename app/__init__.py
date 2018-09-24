from flask import *
from flaskext.mysql import MySQL

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

from app import routes

