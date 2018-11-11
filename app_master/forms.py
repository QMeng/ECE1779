from flask_wtf import FlaskForm
from flask import *
from wtforms import FloatField, IntegerField, SubmitField
from wtforms.validators import *

from app_master.models import AutoScalingConfig


class AutoScalingConfigForm(FlaskForm):
    '''
    Auto Scaling Configuration form
    '''
    scaleUpThreshold = FloatField("Scale Up CPU Threshold", validators=[Optional()])
    scaleDownThreshold = FloatField("Scale Down CPU Threshold", validators=[Optional()])
    scaleUpRatio = IntegerField("Scale Up Ratio", validators=[Optional()])
    scaleDownRatio = IntegerField("Scale Down Ratio", validators=[Optional()])
    submitAutoConfig = SubmitField("Submit Auto Config")


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
    submitManualConfig = SubmitField("Submit Manual Config")
