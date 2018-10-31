from flask_table import *


class InstanceTable(Table):
    name = Col("Worker Name")
    cpuUsage = Col("CPU Utilization")
    items = []

    def __init__(self, items):
        self.items = items

    def sort_url(self, col_id, reverse=False):
        super.sort_url(col_id)


class InstanceInfo(object):
    def __init__(self, name, cpuUsage):
        self.name = name
        self.cpuUsage = cpuUsage
