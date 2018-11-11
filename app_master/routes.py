from app_master import *
from app_master.utilities import *
from app_master.models import *
from app_master.forms import *
from app_worker.models import ImageContents, User
import math


@app_master.route('/')
def index():
    return redirect(url_for('home'))


@app_master.route('/admin', methods=['GET', 'POST'])
def home():
    '''
    Main console for displaying CPU Utilization table, Manual Scaling Config form, Auto Scaling Config form
    '''
    manualScalingForm = ManualScalingConfigForm()
    autoScalingForm = AutoScalingConfigForm()

    # retrieve active worker instances and compute their cpu utilization display table
    instanceIDs = getEC2WorkerInstanceIDs()
    workerTable = computeWorkerTable(instanceIDs)

    # retrieve the auto scaling configuration from remote database
    autoScalingSettings = AutoScalingConfig.query.all()
    if autoScalingSettings == []:
        autoScalingSetting = AutoScalingConfig(AS_UP_RATIO, AS_DOWN_RATIO, AS_UP_THRESHOLD,
                                               AS_DOWN_THRESHOLD)
        db.session.add(autoScalingSetting)
        db.session.commit()
    else:
        autoScalingSetting = autoScalingSettings[0]

    # compute the auto scaling configuration display table
    asItems = [dict(name='Auto Scale Up Ratio', value=autoScalingSetting.scaleUpRatio),
               dict(name='Auto Scale Down Ratio', value=autoScalingSetting.scaleDownRatio),
               dict(name='Auto Scale Up Threshold', value=autoScalingSetting.scaleUpThreshold),
               dict(name='Auto Scale Down Threshold', value=autoScalingSetting.scaleDownThreshold)]
    autoScalingTable = AutoScalingConfigTable(asItems)
    autoScalingTable.border = True

    # since we have 2 forms in this page, need to check which form is the submitted form
    if request.method == 'POST':
        if request.form['form-name']:
            formName = request.form['form-name']

            # the submitted form is manual scaling up form
            if formName == 'manualScalingConfigForm':
                if manualScalingForm.validate_on_submit():
                    manualScalingUp = manualScalingForm.manualScaleUp.data
                    createWorkerInstance(manualScalingUp)
                    return redirect(url_for('home'))

            # the submitted form is auto scaling form
            if formName == 'autoScalingConfigForm':
                if autoScalingForm.validate_on_submit():
                    if validateAutoScalingInputs(autoScalingForm.scaleUpRatio.data, autoScalingForm.scaleDownRatio.data,
                                                 autoScalingForm.scaleUpThreshold.data,
                                                 autoScalingForm.scaleDownThreshold.data):
                        # update the auto scaling settings if any of them is modified thru the form
                        if autoScalingForm.scaleUpRatio.data:
                            autoScalingSetting.set_scaleUpRatio(autoScalingForm.scaleUpRatio.data)
                        if autoScalingForm.scaleDownRatio.data:
                            autoScalingSetting.set_scaleDownRatio(autoScalingForm.scaleDownRatio.data)
                        if autoScalingForm.scaleUpThreshold.data:
                            autoScalingSetting.set_scaleUpThreshhold(autoScalingForm.scaleUpThreshold.data)
                        if autoScalingForm.scaleDownThreshold.data:
                            autoScalingSetting.set_scaleDownThreshold(autoScalingForm.scaleDownThreshold.data)

                        if autoScalingSetting.scaleDownThreshold > autoScalingSetting.scaleUpThreshold:
                            flash("Scale down threshold should be smaller than scale up threshold", 'as_error')
                            db.session.remove()
                        else:
                            db.session.add(autoScalingSetting)
                    db.session.commit()
                    return redirect(url_for('home'))

    return render_template('admin.html', workerTable=workerTable, manualScalingConfigForm=manualScalingForm,
                           autoScalingConfigForm=autoScalingForm, asTable=autoScalingTable)


@app_master.route('/admin/delete/<id>', methods=['POST'])
def destroyWorker(id):
    '''
    Destroy a specific worker instance
    '''
    if PRIMARY_WORKER_ID == id:
        flash("This is the primary worker instance, it should not be terminated, please choose another one!", 'warning')
    else:
        destroyInstance([id])
    return redirect(url_for('home'))


@app_master.route('/admin/reset', methods=['GET'])
def wipeOutEverything():
    '''
    Method to destroy worker instances, wipe out remote database's image table, wipe out S3 buckets
    '''
    # terminate all worker instances
    instanceIDs = getEC2WorkerInstanceIDs()
    if PRIMARY_WORKER_ID in instanceIDs:
        instanceIDs.remove(PRIMARY_WORKER_ID)
    destroyInstance(instanceIDs)

    # wipe out database's image table
    db.session.query(ImageContents).delete()
    db.session.query(User).delete()
    db.session.commit()

    # wipe out S3 buckets
    for bucket in s3_resource.buckets.all():
        for obj in bucket.objects.all():
            obj.delete()
        bucket.delete()

    return redirect(url_for('home'))


def autoScaling():
    '''
    this method will be called by scheduler periodically to perform auto scaling for the worker pool.
    '''
    instanceIDs = getEC2WorkerInstanceIDs()
    instanceInfo = computeWorkerDict(instanceIDs)

    # grab the auto scaling setting from remote database
    autoScalingSettings = AutoScalingConfig.query.all()[0]
    as_up_ratio = autoScalingSettings.scaleUpRatio
    as_down_ratio = autoScalingSettings.scaleDownRatio
    as_up_threshold = autoScalingSettings.scaleUpThreshold
    as_down_threshold = autoScalingSettings.scaleDownThreshold

    average = calculateAverage(instanceInfo)
    print("Current average CPU consumption is: " + str(average))

    if (average > as_up_threshold) and as_up_ratio > 1:
        # if worker pool load is greater than scale up threshold
        # need to scale up the pool
        print("Auto Scaling Up " + str(len(instanceIDs) * (as_up_ratio - 1)) + " instances")
        createWorkerInstance(len(instanceIDs) * (as_up_ratio - 1))

    if (average < as_down_threshold) and as_down_ratio > 1 and len(instanceIDs) > 1:
        # if worker pool is below scale down threshhold
        # need to destroy workers with least loads
        numToDestroy = math.ceil(len(instanceIDs) / (as_down_ratio))
        if numToDestroy > len(instanceIDs):
            numToDestroy = len(instanceIDs) - 1
        instanceToDestroy = []
        for i in range(numToDestroy):
            if instanceInfo[i][0] == PRIMARY_WORKER_ID:
                instanceInfo.pop(i)
            instanceToDestroy.append(instanceInfo[i][0])
        print("Auto scaling down " + str(len(instanceToDestroy)) + " instances")
        destroyInstance(instanceToDestroy)
