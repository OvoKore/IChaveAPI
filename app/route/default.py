from flask import Blueprint, jsonify, current_app

bp_default = Blueprint('default', __name__)

@bp_default.route('/', defaults={'path': ''})
@bp_default.route('/<path:path>')
def catch_all(path):
    return jsonify({'msg': 'Welcome to IChave API!'})
