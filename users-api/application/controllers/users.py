from flask import abort, jsonify, Blueprint, request
from sqlalchemy.sql.expression import func
from database import db_session
from models import Users
from factories.log import create_logger


users_blueprint = Blueprint('users', __name__)
log = create_logger('users-api')


@users_blueprint.route("/random/user")
def random_user():
    u = Users.query.order_by(func.random()).limit(1).one_or_none()
    if not u:
        abort(404, "user not found")
    return jsonify(u.to_dict())


@users_blueprint.route("/user/comments/<username>")
def comments(username):
    u = Users.query.filter(Users.name == username).one_or_none()
    if not u:
        abort(404, "user not found")
    return jsonify(u.to_dict())


@users_blueprint.route("/users")
def users():
    return jsonify([x[0] for x in db_session.query(Users.name).all()])


@users_blueprint.route("/healthcheck")
def healthcheck():
    log.info(f"Healthcheck source address: {request.remote_addr}")
    return jsonify({})
