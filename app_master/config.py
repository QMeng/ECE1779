import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ece1779pass@localhost/ECE1779'
    SQLALCHEMY_TRACK_MODIFICATIONS = False