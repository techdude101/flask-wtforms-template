from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DeviceInfoForm(FlaskForm):
    device_name = StringField("device_name_placeholder",
                              validators=[DataRequired()])
    description = StringField("description_placeholder")
    submit = SubmitField('submit_button_text')
