import os

REMOTE_DB_IP = '34.227.106.100'

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ece1779pass@' + REMOTE_DB_IP + '/ECE1779'
    SQLALCHEMY_TRACK_MODIFICATIONS = False