from flask_table import *
from app_master import *


class InstanceTable(Table):
    '''
    Flask Table for diaplay of the instances
    '''
    id = Col("Id", show=False)
    name = Col("Worker Name")
    instanceId = Col("Instance ID")
    cpuUsage = Col("CPU Utilization")
    destroy = ButtonCol("Destroy", 'destroyWorker', url_kwargs=dict(id='instanceId'))
    items = []

    def __init__(self, items):
        self.items = items

    def sort_url(self, col_id, reverse=False):
        super.sort_url(col_id)


class AutoScalingConfigTable(Table):
    '''
    Flask Table for display of auto scaling configurations
    '''
    id = Col("Id", show=False)
    name = Col("Name")
    value = Col("Value")

    def sort_url(self, col_id, reverse=False):
        super.sort_url(col_id)


class InstanceInfo(object):
    '''
    Information of instance
    '''

    def __init__(self, name, instanceId, cpuUsage):
        self.name = name
        self.instanceId = instanceId
        self.cpuUsage = cpuUsage


class AutoScalingConfig(db.Model):
    '''
    Auto Scaling Conguration table in database. This table is used to store the auto scaling config settings.
    '''
    __tablename__ = "AutoScalingConfig"
    id = db.Column(db.Integer, primary_key=True)
    scaleUpRatio = db.Column(db.Integer)
    scaleDownRatio = db.Column(db.Integer)
    scaleUpThreshold = db.Column(db.Float)
    scaleDownThreshold = db.Column(db.Float)

    def __init__(self, scaleUpRatio, scaleDownRatio, scaleUpThreshold, scaleDownThreshold):
        self.scaleUpRatio = scaleUpRatio
        self.scaleDownRatio = scaleDownRatio
        self.scaleUpThreshold = scaleUpThreshold
        self.scaleDownThreshold = scaleDownThreshold

    def set_scaleUpRatio(self, scaleUpRatio):
        self.scaleUpRatio = scaleUpRatio

    def set_scaleDownRatio(self, scaleDownRatio):
        self.scaleDownRatio = scaleDownRatio

    def set_scaleUpThreshhold(self, scaleUpThreshhold):
        self.scaleUpThreshold = scaleUpThreshhold

    def set_scaleDownThreshold(self, scaleDownThreshold):
        self.scaleDownThreshold = scaleDownThreshold
