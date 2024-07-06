from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class SensorInfoForm(FlaskForm):
    sensor_name = StringField('sensor_name_placeholder',
                              validators=[DataRequired()])
    temperature = StringField("temperature_placeholder",
                              validators=[DataRequired()])
    humidity = IntegerField('humidity_placeholder',
                            validators=[DataRequired()])
    submit = SubmitField('submit_button_text')
