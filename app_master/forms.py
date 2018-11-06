from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField
from wtforms.validators import *


class AutoScalingConfigForm(FlaskForm):
    '''
    Auto Scaling Configuration form
    '''
    scaleUpThreshhold = FloatField("Scale Up CPU Threshhold")
    scaleDownThreshhold = FloatField("Scale Down CPU Threshhold")
    scaleUpRatio = FloatField("Scale Up Ratio")
    scaleDownRatio = FloatField("Scale Down Ratio")
    submit = SubmitField("Submit")


class RefreshCurrentPageForm(FlaskForm):
    '''
    A simple form for refreshing current page
    '''
    refresh = SubmitField("Refresh Table")


class ManualScalingConfigForm(FlaskForm):
    '''
    Manual Scaling Configuration form
    '''
    manualScaleUp = IntegerField("Manual Scale Up",
                                 validators=[DataRequired(),
                                             NumberRange(min=1, max=5,
                                                         message='Please input a number between 1 and 5')])
    submitConfig = SubmitField("Submit Manual Config")
