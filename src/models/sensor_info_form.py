from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class SensorInfoForm(FlaskForm):
    sensor_name = StringField("Sensor Name", validators=[DataRequired()])
    temperature = DecimalField("Temperature (°C)",
                               validators=[DataRequired()],
                               places=1)
    humidity = IntegerField("Humidity (%)", validators=[DataRequired()])
    submit = SubmitField("Save")
