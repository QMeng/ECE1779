import os

REMOTE_DB_IP = '34.227.106.100'


class Config(object):
    '''This class stores the configurations for this app_worker'''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://damonmeng:ece1779pass@' + REMOTE_DB_IP + '/ECE1779'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


AWS_CONNECTION_ARGS = {
    'aws_access_key_id': 'AKIAJWUAQXN3NJPBWZBQ',
    'aws_secret_access_key': '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',
    'region_name': 'us-east-1'
}
