from app_master import *


@app_master.route('/')
@app_master.route('/admin', methods=['GET', 'POST'])
def home():
    pass


@app_master.route('/admin/configAS')
def configAutoScaling():
    pass