from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, get_jwt_identity
from functools import wraps
from flask import jsonify

jwt = JWTManager()

def configure(app):
    jwt.init_app(app)
    app.jwt = jwt

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if get_jwt_claims().get('role', None) != 'user' or get_jwt_identity() is None:
            return jsonify({ 'msg': 'Unauthorized, invalid credentials' }), 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def locksmith_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if get_jwt_claims().get('role', None) != 'locksmith' or get_jwt_identity() is None:
            return jsonify({ 'msg': 'Unauthorized, invalid credentials' }), 403
        else:
            return fn(*args, **kwargs)
    return wrapper
