import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MYSQL_DATABASE_HOST = "localhost"
    MYSQL_DATABASE_USER = "root"
    MYSQL_DATABASE_PASSWORD = "BelieveMe1314"
    MYSQL_DATABASE_DB = "ECE1779A1"
    MYSQL_CURSORCLASS = "DictCursor"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:BelieveMe1314@localhost/ECE1779A2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False