import os

REMOTE_DB_IP = '34.202.92.63'


class Config(object):
    '''This class stores the configurations for this app_worker'''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


AWS_CONNECTION_ARGS = {
    'aws_access_key_id': 'AKIAJDJ6ORD4VH6Z45DA',
    'aws_secret_access_key': '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',
    'region_name': 'us-east-1'
}
