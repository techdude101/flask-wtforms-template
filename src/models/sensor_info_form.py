from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class SensorInfoForm(FlaskForm):
    sensor_name = StringField("Sensor", validators=[DataRequired()])
    temperature = DecimalField("Temperature (°C)", validators=[DataRequired()])
    humidity = IntegerField("Humidity (%)", validators=[DataRequired()])
    submit = SubmitField("Save")
