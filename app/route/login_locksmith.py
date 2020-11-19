from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from app.model.locksmith import Locksmith
from app.serializer.locksmith import LocksmithSchema
from app.util import decrypt

bp_login_locksmith = Blueprint('login_locksmith', __name__)

@bp_login_locksmith.route('/login-locksmith', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if email is None or password is None:
        return jsonify({'msg': 'Missing email or password'}), 400
        
    locksmith = Locksmith.query.filter(Locksmith.email==email).first()
    if locksmith and locksmith.verify_password(decrypt(password)):
        return jsonify({
            'access_token': create_access_token(
                identity = locksmith.id,
                fresh = timedelta(minutes = 15),
                expires_delta = timedelta(hours = 24),
                user_claims = {'role':'locksmith'}
            ),
            'refresh_token': create_refresh_token(
                identity = locksmith.id,
                expires_delta = timedelta(days=7),
                user_claims = {'role':'locksmith'}
            ),
            'fresh': str(datetime.utcnow() + timedelta(minutes = 15)),
            'expires_access': str(datetime.utcnow() + timedelta(hours = 24)),
            'expires_refresh': str(datetime.utcnow() + timedelta(days = 7)),
            'msg': 'sucess'
        }), 200

    return jsonify({
        'msg': 'Unauthorized, invalid credentials'
    }), 401
