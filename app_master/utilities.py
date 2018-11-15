from app_master import *
import time
from datetime import datetime, timedelta
from app_master.config import *
from app_master.models import InstanceInfo, InstanceTable


def getEC2WorkerInstanceIDs():
    '''
    return a list of ids of the current running instances
    '''
    result = []
    instances = ec2_resource.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']},
                 {'Name': 'tag-value', 'Values': ['ECE1779Worker', 'ECE1779PrimaryWorker']}, ])

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


def computeWorkerDict(instanceIDs):
    '''
    :return: a sorted dictionary of all the instance's cpu usage
    '''
    listOfWorker = {}
    for i in range(len(instanceIDs)):
        cpuAverage = getInstanceCPUUtilization(instanceIDs[i])
        listOfWorker[instanceIDs[i]] = cpuAverage
    listOfWorker = sorted(listOfWorker.items(), key=lambda kv: kv[1])
    return listOfWorker


def createWorkerInstance(numInstance):
    '''
    create a specific number of worker instances, and register them to the CLB
    '''
    instances = ec2_resource.create_instances(ImageId=AMI_ID,
                                              InstanceType=WORKER_INSTANCE_TYPE,
                                              SecurityGroups=SECURITY_GROUP,
                                              KeyName=KEY_NAME,
                                              UserData=USER_DATA,
                                              Monitoring={'Enabled': True},
                                              MinCount=1,
                                              MaxCount=numInstance)
    idList = []
    registerIdList = []

    for instance in instances:
        idList.append(instance.id)
        registerIdList.append({'InstanceId': instance.id})

    waitForInstancesRunning(idList)

    ec2_resource.create_tags(Resources=idList, Tags=[{'Key': 'Name', 'Value': 'ECE1779Worker'}])
    elb_client.register_instances_with_load_balancer(LoadBalancerName=LOAD_BALANCER_NAME, Instances=registerIdList)
    waitForInstancesHealthy(idList)


def destroyInstance(instanceIDs):
    '''
    delete a specific instance, deregister the instances from CLB before terminatings
    '''
    deregisterIdList = []
    for instanceID in instanceIDs:
        deregisterIdList.append({'InstanceId': instanceID})

    if deregisterIdList != []:
        elb_client.deregister_instances_from_load_balancer(LoadBalancerName=LOAD_BALANCER_NAME,
                                                           Instances=deregisterIdList)

    if instanceIDs != []:
        ec2_client.terminate_instances(InstanceIds=instanceIDs, DryRun=False)


def waitForInstancesRunning(idList):
    '''
    wait for instances to be in running state
    '''
    while not isAllInstanceRunning(idList):
        time.sleep(5)
        print("Waiting for instances to be running")
    print("All instances are running now")


def waitForInstancesHealthy(idList):
    '''
    wait for instances to be healthy in load balancer
    '''
    counter = 0
    while not isAllInstanceHealthy(idList):
        time.sleep(5)
        print("Waiting for instances in CLB to be healthy")
        if counter == 30:
            break
        counter += 5
    print("All instances are healthy now")


def isAllInstanceHealthy(idList):
    '''
    check if instances are healthy in load balancer
    '''
    status = True
    for instanceId in idList:
        response = elb_client.describe_instance_health(LoadBalancerName=LOAD_BALANCER_NAME,
                                                       Instances=[{'InstanceId': instanceId}])
        if response['InstanceStates'][0]['State'] != 'InService':
            return False
    return status


def isAllInstanceRunning(idList):
    '''
    check if instances are running
    '''
    for i in idList:
        ins = ec2_resource.Instance(i)
        if ins.state['Name'] == 'pending':
            return False
    return True


def calculateAverage(instances):
    '''
    return the average cpu usage of instances
    '''
    if len(instances) == 0:
        return 0

    total = 0
    for (id, value) in instances:
        total += value

    return 1.0 * total / len(instances)


def validateAutoScalingInputs(asUpRatio, asDownRatio, asUpThreshold, asDownThreshold):
    '''
    :return: true if the values inputed satisfies the auto scaling constraints
    '''
    rc = 1
    if (not asUpRatio) and (not asDownRatio) and (not asUpThreshold) and (not asDownThreshold):
        flash("Please fill out at least one of the fields!", 'as_error')
        rc = 0
    if (asUpRatio) and (asUpRatio < 1):
        flash("Auto Scaling Up Ratio should be an integer greater than 1!", 'as_error')
        rc = 0
    if (asDownRatio) and (asDownRatio < 1):
        flash("Auto Scaling Down Ratio should be an integer greater than 1!", 'as_error')
        rc = 0
    if (asUpThreshold) and (asUpThreshold < 0 or asUpThreshold > 100):
        flash("Auto Scaling Up Threshold should be an float between 0 and 100")
        rc = 0
    if (asDownThreshold) and (asDownThreshold < 0 or asDownThreshold > 100):
        flash("Auto Scaling Down Threshold should be an float between 0 and 100")
        rc = 0

    return rc == 1
