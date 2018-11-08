from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField
from wtforms.validators import *


class AutoScalingConfigForm(FlaskForm):
    '''
    Auto Scaling Configuration form
    '''
    scaleUpThreshold = FloatField("Scale Up CPU Threshold", validators=[Optional()])
    scaleDownThreshold = FloatField("Scale Down CPU Threshold", validators=[Optional()])
    scaleUpRatio = IntegerField("Scale Up Ratio", validators=[Optional()])
    scaleDownRatio = IntegerField("Scale Down Ratio", validators=[Optional()])
    submitAutoConfig = SubmitField("Submit Auto Config")

    def validate(self):
        if (not self.scaleDownRatio.data) and (not self.scaleUpRatio.data) and (not self.scaleDownThreshold.data) and (
                not self.scaleUpThreshold.data):
            errMsg = "At least one of the field should be filled!"
            self.scaleDownRatio.errors.append(errMsg)
            self.scaleUpRatio.errors.append(errMsg)
            self.scaleDownThreshold.errors.append(errMsg)
            self.scaleUpThreshold.errors.append(errMsg)
            return False
        return True


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
