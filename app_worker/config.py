import os


class Config(object):
    '''This class stores the configurations for this app_worker'''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MYSQL_DATABASE_HOST = "localhost"
    MYSQL_DATABASE_USER = "root"
    MYSQL_DATABASE_PASSWORD = "ece1779pass"
    MYSQL_DATABASE_DB = "ECE1779"
    MYSQL_CURSORCLASS = "DictCursor"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ece1779pass@localhost/ECE1779'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


AWS_CONNECTION_ARGS = {
    'aws_access_key_id': 'AKIAI6ZO5JW7NNN6V2XA',
    'aws_secret_access_key': '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',
    'region_name': 'us-east-1'
}
