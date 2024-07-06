from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DeviceInfoForm(FlaskForm):
    device_name = StringField("Device Name", validators=[DataRequired()])
    description = StringField("Description")
    submit = SubmitField("Save")
