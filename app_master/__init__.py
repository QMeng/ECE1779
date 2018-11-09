from flask import *
from app_master.config import *
from flask_sqlalchemy import *
import boto3

app_master = Flask(__name__)
app_master.config.from_object(Config)

db = SQLAlchemy(app_master)

cw_client = boto3.client('cloudwatch', **AWS_CONNECTION_ARGS)
ec2_resource = boto3.resource('ec2', **AWS_CONNECTION_ARGS)
ec2_client = boto3.client('ec2', **AWS_CONNECTION_ARGS)
s3_resource = boto3.resource('s3', **AWS_CONNECTION_ARGS)
elb_client = boto3.client('elb', **AWS_CONNECTION_ARGS)

from app_master import routes
