from flask import Flask

from griminventory_api.api.items import items
from griminventory_api.api.status import status


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(items)
    app.register_blueprint(status)
    return app
