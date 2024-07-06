"""Log level routes"""

import logging
from flask import Blueprint, jsonify, current_app, request
from flask_babel import _

log_level_route = Blueprint(
    "log_level", __name__, template_folder=None, url_prefix="/log-level"
)


@log_level_route.route("/debug", methods=["GET"])
def handle_debug():
    """Log level info endpoint"""

    current_app.logger.debug(request.url)
    log_level = current_app.logger.getEffectiveLevel()

    response = {_("log level"): logging.getLevelName(log_level)}

    return jsonify(response), 200


@log_level_route.route("/info", methods=["GET"])
def handle_info():
    """Log level info endpoint"""

    current_app.logger.info(request.url)
    log_level = current_app.logger.getEffectiveLevel()

    response = {_("log level"): logging.getLevelName(log_level)}

    return jsonify(response), 200


@log_level_route.route("/warning", methods=["GET"])
def handle_warning():
    """Log level warning endpoint"""

    current_app.logger.warning(request.url)
    log_level = current_app.logger.getEffectiveLevel()

    response = {_("log level"): logging.getLevelName(log_level)}

    return jsonify(response), 200


@log_level_route.route("/error", methods=["GET"])
def handle_error():
    """Log level error endpoint"""

    current_app.logger.error(request.url)
    log_level = current_app.logger.getEffectiveLevel()

    response = {_("log level"): logging.getLevelName(log_level)}

    return jsonify(response), 200


@log_level_route.route("/critical", methods=["GET"])
def handle_critical():
    """Log level critical endpoint"""

    current_app.logger.critical(request.url)
    log_level = current_app.logger.getEffectiveLevel()

    response = {_("log level"): logging.getLevelName(log_level)}

    return jsonify(response), 200
