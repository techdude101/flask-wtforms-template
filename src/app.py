"""Main Flask application"""

import argparse
import os
import sys
import socket
import logging
import logging.config
import textwrap
from flask import Flask, request, session, g, render_template
from flask_babel import Babel
from models.device_info_form import DeviceInfoForm
from models.sensor_info_form import SensorInfoForm

# Routes
from routes.hw import hw_route
from routes.log_level import log_level_route


DOCKER_STDOUT_PATH = "/proc/1/fd/1"
SUPPORTED_LOCALES = ["en", "en_GB", "fr"]

log_config_docker = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s %(levelname)s in %(module)s: %(message)s]",  # noqa: E501
        }
    },
    "handlers": {
        "console": {
            "class": "logging.FileHandler",
            "filename": DOCKER_STDOUT_PATH,
            "formatter": "default",
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}

device_info = {
    "device_name": "ESP32",
    "description": ""
}

sensor_info = {
    "sensor_name": "abc123",
    "temperature": -99.0,
    "humidity": 199
}


def get_locale():
    # Check if the language query parameter is set and valid
    if "lang" in request.args:
        lang = request.args.get("lang")
        if lang in SUPPORTED_LOCALES:
            session["lang"] = lang
            return session["lang"]
    # If not set via query, check if we have it stored in the session
    elif "lang" in session:
        return session.get("lang")
    # Otherwise, use the browser's preferred language
    return request.accept_languages.best_match(SUPPORTED_LOCALES)


def get_timezone():
    user = getattr(g, "user", None)
    if user is not None:
        return user.timezone


def create_app():
    """Create the main flask app"""

    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = "my super secret key"
    flask_app.register_blueprint(hw_route)
    flask_app.register_blueprint(log_level_route)
    Babel(flask_app, locale_selector=get_locale,
          timezone_selector=get_timezone)

    return flask_app


app = create_app()


@app.route("/")
def hello_world():

    locales = request.headers.get("Accept-Language")

    app.logger.debug(request.headers)
    app.logger.debug(locales)
    return render_template('hw.html', current_locale=get_locale())


@app.route("/device", methods=["GET", "POST"])
def device():
    device_info_form = DeviceInfoForm(data=device_info)

    if device_info_form.validate_on_submit():
        device_info["device_name"] = device_info_form.device_name.data
        device_info["description"] = device_info_form.description.data
        device_info_form.description.data = ''
        device_info_form.device_name.data = ''

    return render_template("device_info_form.html",
                           device_info=device_info,
                           form=device_info_form,
                           current_locale=get_locale())


@app.route("/sensor", methods=["GET", "POST"])
def sensor():
    sensor_info_form = SensorInfoForm(data=sensor_info)

    if sensor_info_form.validate_on_submit():
        sensor_info["sensor_name"] = sensor_info_form.sensor_name.data
        sensor_info["temperature"] = sensor_info_form.temperature.data
        sensor_info["humidity"] = sensor_info_form.humidity.data

    return render_template("sensor_info_form.html",
                           sensor_info=sensor_info,
                           form=sensor_info_form,
                           current_locale=get_locale())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--host", default="127.0.0.1",
                        help="Listening host")
    parser.add_argument("--port", default=8080, help="Listening port")
    parser.add_argument("--debug", action="store_true", help="Debug flag")
    parser.add_argument(
        "-l",
        "--log-level",
        default="ERROR",
        help=textwrap.dedent(
            """\
                        CRITICAL, ERROR, WARNING, INFO or DEBUG
        """
        ),
    )

    args = parser.parse_args()

    if os.path.exists(DOCKER_STDOUT_PATH):
        logging.config.dictConfig(log_config_docker)

    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(args.log_level)

    host = args.host
    port = args.port

    try:
        port = int(port)
        if port > 65535 or port < 10:
            raise ValueError("Invalid listening port")
    except ValueError:
        app.logger.error("Invalid listening port")
        sys.exit(-1)

    if type(port) is not int:
        app.logger.error("Invalid listening port")
        sys.exit(-1)

    try:
        app.logger.info("Startup .. %s %s", host, port)
        app.run(host=host, port=port, debug=args.debug)
    except socket.gaierror as ge:
        app.logger.error(ge)
        sys.exit(-1)
