import os
from flask import Flask, jsonify
from flask.logging import default_handler
from config import get_config


def create_application():
    app = Flask(__name__)
    config = get_config(os.getenv('CONFIG_ENV', 'dev'))
    app.config.from_object(config)
    app.logger.removeHandler(default_handler)

    from controllers.product import product_api
    app.register_blueprint(product_api)

    simple_errors = (400, 401, 404, 403)

    def simple_error(e):
        return jsonify({'error': e.code, 'message': e.description}), e.code

    for error in simple_errors:
        app.errorhandler(error)(simple_error)

    return app
