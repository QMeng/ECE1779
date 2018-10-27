from flask import *
from app_master.config import Config

app_master = Flask(__name__)
app_master.config.from_object(Config)

from app_master import routes
