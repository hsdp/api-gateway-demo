from flask import Flask, request, jsonify
from flask.logging import default_handler
from config import Config
from .log import create_logger


def create_application():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.logger.removeHandler(default_handler)

    from controllers.users import users_blueprint
    app.register_blueprint(users_blueprint)

    simple_errors = (400, 401, 404, 403)

    def simple_error(e):
        return jsonify(error=e.code, message=e.description), e.code

    for error in simple_errors:
        app.errorhandler(error)(simple_error)

    from database import db_session, init_db
    if app.config['INITDB']:
        init_db()

    def remove_db_session(e):
        if e is not None:
            logger = create_logger('users-api')
            logger.info('Teardown Request Exception: {}'.format(e))
        db_session.remove()

    app.teardown_request(remove_db_session)
    return app
