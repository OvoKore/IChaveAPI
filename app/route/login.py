from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from app.model.user import User
from app.serializer.user import UserSchema
from app.util import decrypt

bp_login = Blueprint('login', __name__)

@bp_login.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if email is None or password is None:
        return jsonify({'msg': 'Missing email or password'}), 400

    password = decrypt(password)

    user = User.query.filter(User.email==email).first()
    if user and user.verify_password(password):
        return jsonify({
            'access_token': create_access_token(
                identity = user.id,
                fresh = timedelta(minutes = 15),
                expires_delta = timedelta(hours = 24),
                user_claims = {'role':'user'}
            ),
            'refresh_token': create_refresh_token(
                identity = user.id,
                expires_delta = timedelta(days=7),
                user_claims = {'role':'user'}
            ),
            'fresh': str(datetime.utcnow() + timedelta(minutes = 15)),
            'expires_access': str(datetime.utcnow() + timedelta(hours = 24)),
            'expires_refresh': str(datetime.utcnow() + timedelta(days = 7)),
            'msg': 'sucess'
        }), 200

    return jsonify({
        'msg': 'Unauthorized, invalid credentials'
    }), 401