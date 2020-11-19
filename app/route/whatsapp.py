from flask import Blueprint, request, jsonify, current_app
from app.model.user import User as md
from app.serializer.user import UserSchema as ma
from app.jwt import user_required
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import and_
import json
from app.model.service import Service
from app.serializer.service import ServiceSchema

bp_whatsapp = Blueprint('whatsapp', __name__)

@bp_whatsapp.route('/get-whatsapp-url', methods=['GET'])
@user_required
def get_whatsapp_url():
    _filter = md.id == get_jwt_identity()
    result = md.query.filter(_filter).first()
    user = json.loads(ma(many=False).dumps(result))
    _filter = Service.id == request.json
    result = Service.query.filter(_filter).first()
    serv = json.loads(ServiceSchema(many=False).dumps(result))
    url = f"https://api.whatsapp.com/send?phone=+55{user['cell_phone']}&text=Olá, me chamo {user['name']} e tenho interesse no seguinte serviço:\n{serv['name']}"
    return jsonify({'msg': url}), 200