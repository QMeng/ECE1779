from flask_table import *


class InstanceTable(Table):
    id = Col('Id', show=False)
    name = Col("Worker Name")
    instanceId = Col("Instance ID")
    cpuUsage = Col("CPU Utilization")
    destroy = ButtonCol("Destroy", 'destroyWorker', url_kwargs=dict(id='instanceId'))
    items = []

    def __init__(self, items):
        self.items = items

    def sort_url(self, col_id, reverse=False):
        super.sort_url(col_id)


class InstanceInfo(object):
    def __init__(self, name, instanceId, cpuUsage):
        self.name = name
        self.instanceId = instanceId
        self.cpuUsage = cpuUsage
