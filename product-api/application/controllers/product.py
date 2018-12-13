from redis import Redis
from flask import jsonify, Blueprint, current_app, abort


product_api = Blueprint('product_api', __name__)


@product_api.route('/healthcheck')
def healthcheck():
    return jsonify({})


@product_api.route('/products')
def products():
    r = Redis(**current_app.config['REDIS_CREDS'])
    return jsonify({'products': [k.decode('utf-8') for k in r.keys()]})


@product_api.route('/random/product')
def random_product():
    r = Redis(**current_app.config['REDIS_CREDS'])
    random_key = r.randomkey()
    if not random_key:
        abort(404, "There are no products!")
    return jsonify({random_key.decode('utf-8'): r.get(random_key).decode('utf-8')})


@product_api.route('/product/<guid>')
def get_product(guid):
    r = Redis(**current_app.config['REDIS_CREDS'])
    product = r.get(guid)
    if not product:
        abort(404, "Product does not exist")
    return jsonify({guid: product.decode('utf-8')})
