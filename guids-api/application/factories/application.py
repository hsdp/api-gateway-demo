from flask import Flask, request, jsonify
from flask.logging import default_handler
from utils import generate_data
from config import Config


def create_application():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.logger.removeHandler(default_handler)

    generate_data(app.config['JSON_TMP_FILE'])

    from controllers.guids import guids_blueprint
    app.register_blueprint(guids_blueprint)

    simple_errors = (400, 401, 404, 403)

    def simple_error(e):
        return jsonify(error=e.code, message=e.description), e.code

    for error in simple_errors:
        app.errorhandler(error)(simple_error)

    return app
