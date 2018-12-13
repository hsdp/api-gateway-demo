from flask import jsonify, Blueprint, Response, current_app


guids_blueprint = Blueprint('guids', __name__)


@guids_blueprint.route('/')
def index():

    def read_file(filename):
        with open(filename) as f:
            for chunk in f:
                yield chunk

    return Response(read_file(current_app.config['JSON_TMP_FILE']))


@guids_blueprint.route('/healthcheck')
def healthcheck():
    return jsonify({})
