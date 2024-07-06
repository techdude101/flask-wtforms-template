"""Hello world route"""

from flask import Blueprint, jsonify, current_app, request
from flask_babel import _

hw_route = Blueprint("hw", __name__, template_folder=None)


@hw_route.route("/hw", methods=["GET"])
def handle_hw():
    """Hello world endpoint"""

    current_app.logger.info("/hw")
    current_app.logger.debug(request.get_data())

    return jsonify(_('hello_world')), 200
