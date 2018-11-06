from app_master import *
from app_master.utilities import *
from app_master.models import *
from app_master.forms import *


@app_master.route('/')
def index():
    return redirect(url_for('home'))


@app_master.route('/admin', methods=['GET', 'POST'])
def home():
    '''
    Main console for displaying CPU Utilization table, Manual Scaling Config form, Auto Scaling Config form
    '''
    refreshForm = RefreshCurrentPageForm()
    manualScalingForm = ManualScalingConfigForm()

    instanceIDs = getEC2InstanceIDs()
    workerTable = computeWorkerTable(instanceIDs)

    if request.method == 'POST':
        if request.form['form-name']:
            formName = request.form['form-name']
            if formName == 'manualScalingConfigForm':
                if manualScalingForm.validate_on_submit():
                    manualScalingUp = manualScalingForm.manualScaleUp.data
                    createWorkerInstance(manualScalingUp)
                    return redirect(url_for('home'))
            if formName == 'refreshForm':
                return redirect(url_for('home'))

    return render_template('admin.html', workerTable=workerTable, refreshForm=refreshForm,
                           manualScalingConfigForm=manualScalingForm)


@app_master.route('/admin/configAutoScaling')
def configAutoScaling():
    pass


@app_master.route('/admin/delete/<id>', methods=['POST'])
def destroyWorker(id):
    destroyInstance(id)
    return redirect(url_for('home'))
