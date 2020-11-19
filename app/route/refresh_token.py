from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, create_refresh_token, get_jwt_identity, get_jwt_claims
from datetime import datetime, timedelta

bp_refresh_token = Blueprint('refresh_token', __name__)

@bp_refresh_token.route('/refresh-token', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    return jsonify({
        'access_token': create_access_token(
            identity = get_jwt_identity(),
            fresh = timedelta(minutes = 15),
            expires_delta = timedelta(hours = 24),
            user_claims = {'role':get_jwt_claims().get('role', None)}
        ),
        'refresh_token': create_refresh_token(
            identity = get_jwt_identity(),
            expires_delta = timedelta(days=7),
            user_claims = {'role':get_jwt_claims().get('role', None)}
        ),
        'fresh': str(datetime.utcnow() + timedelta(minutes = 15)),
        'expires_access': str(datetime.utcnow() + timedelta(hours = 24)),
        'expires_refresh': str(datetime.utcnow() + timedelta(days = 7)),
        'msg': 'sucess'
    }), 200