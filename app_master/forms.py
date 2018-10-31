from flask_wtf import *
from wtforms import StringField, SubmitField, BooleanField


class AutoScalingConfigForm(FlaskForm):
    '''
    Auto Scaling Configuration form
    '''
    scaleUpThreshhold = StringField("Scale Up CPU Threshhold")
    scaleDownThreshhold = StringField("Scale Down CPU Threshhold")
    scaleUpRatio = StringField("Scale Up Ratio")
    scaleDownRatio = StringField("Scale Down Ratio")
    submit = SubmitField("Submit")


class ManualScalingConfigForm(FlaskForm):
    '''
    Manual Scaling Configuration form
    '''
    manualScaleUp = BooleanField("Manual Scale Up")
    manualScaleDown = BooleanField("Manual Scale Down")
    submit = SubmitField("Submit")