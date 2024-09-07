import datetime

from flask import Response, jsonify, Blueprint

status = Blueprint("status", __name__)


@status.route("/v1/status", methods=["GET"])
def status_endpoint() -> Response:
    return jsonify({"timestamp": datetime.datetime.isoformat(datetime.datetime.now(datetime.UTC))})
