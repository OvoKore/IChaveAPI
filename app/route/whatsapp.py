from flask import Blueprint, request, jsonify, current_app
from app.jwt import user_required
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import and_
import json
from app.model.user import User
from app.serializer.user import UserSchema
from app.model.service import Service
from app.serializer.service import ServiceSchema
from app.model.locksmith import Locksmith
from app.serializer.locksmith import LocksmithSchema

bp_whatsapp = Blueprint('whatsapp', __name__)

@bp_whatsapp.route('/get-whatsapp-url', methods=['GET'])
@user_required
def get_whatsapp_url():
    _filter = User.id == get_jwt_identity()
    result = User.query.filter(_filter).first()
    user = json.loads(UserSchema(many=False).dumps(result))
    
    _filter = Service.id == request.json
    result = Service.query.filter(_filter).first()
    serv = json.loads(ServiceSchema(many=False).dumps(result))
    
    _filter = Locksmith.id == serv['locksmith_id']
    result = Locksmith.query.filter(_filter).first()
    lock = json.loads(LocksmithSchema(many=False).dumps(result))
    
    url = f"https://api.whatsapp.com/send?phone=+55{lock['cell_phone']}&text=Olá, me chamo {user['name']} e tenho interesse no seguinte serviço:\n{serv['name']}"
    return jsonify({'msg': url}), 200