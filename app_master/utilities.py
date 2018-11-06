from app_master import *
from datetime import *
from app_master.config import *

from app_master.models import InstanceInfo, InstanceTable


def getEC2InstanceIDs():
    '''
    return a list of ids of the current running instances
    '''
    result = []
    instances = ec2_resource.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    for instance in instances:
        result.append(instance.id)

    return result


def getInstanceCPUUtilization(instanceID):
    '''
    get the instance's CPU utilization
    '''
    response = cw_client.get_metric_statistics(Period=1 * 60,
                                               StartTime=datetime.utcnow() - timedelta(seconds=10 * 60),
                                               EndTime=datetime.utcnow() - timedelta(seconds=0 * 60),
                                               MetricName='CPUUtilization',
                                               Namespace='AWS/EC2',
                                               Unit='Percent',
                                               Statistics=['Average'],
                                               Dimensions=[{'Name': 'InstanceId', 'Value': instanceID}])

    total = 0.0
    for datapoint in response['Datapoints']:
        if 'Average' in datapoint:
            total += datapoint['Average']

    if len(response['Datapoints']) == 0:
        return 0

    return total / len(response['Datapoints'])


def computeWorkerTable(instanceIDs):
    '''
    computing the workers cpu utilization table
    '''
    listOfWorker = []
    for i in range(len(instanceIDs)):
        cpuAverage = getInstanceCPUUtilization(instanceIDs[i])
        worker = InstanceInfo("Worker " + str(i), instanceIDs[i], str(cpuAverage))
        listOfWorker.append(worker)
    workerTable = InstanceTable(listOfWorker)
    workerTable.border = True
    return workerTable


def createWorkerInstance(numInstance):
    '''
    create a specific number of worker instances
    '''
    instances = ec2_resource.create_instances(ImageId=AMI_ID,
                                              InstanceType=WORKER_INSTANCE_TYPE,
                                              SecurityGroups=SECURITY_GROUP,
                                              KeyName=KEY_NAME,
                                              Monitoring={'Enabled': True},
                                              MinCount=1,
                                              MaxCount=numInstance)
    idList = []
    for instance in instances:
        idList.append(instance.id)

    waitForInstancesRunning(idList)

    ec2_resource.create_tags(Resources=idList, Tags=[{'Key': 'Name', 'Value': 'ECE1779Worker'}])


def destroyInstance(instanceID):
    '''
    delete a specific instance
    '''
    ec2_client.terminate_instances(InstanceIds=[instanceID], DryRun=False)


def waitForInstancesRunning(idList):
    '''
    wait for instances to be in running state
    '''
    while not isAllInstanceRunning(idList):
        time.sleep(5)
        print("Waiting for instances to be running")
    print("All instances are running now")


def isAllInstanceRunning(idList):
    '''
    check if instances are running
    '''
    for i in idList:
        ins = ec2_resource.Instance(i)
        if ins.state['Name'] == 'pending':
            return False
    return True
