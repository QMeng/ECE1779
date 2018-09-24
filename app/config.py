import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MYSQL_DATABASE_HOST = "localhost"
    MYSQL_DATABASE_USER = "root"
    MYSQL_DATABASE_PASSWORD = "ece1779pass"
    MYSQL_DATABASE_DB = "ECE1779A1"
    MYSQL_CURSORCLASS = "DictCursor"