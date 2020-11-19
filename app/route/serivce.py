from flask import Blueprint, request, jsonify, current_app
from app.serializer.service import ServiceSchema as ma
from app.model.service import Service as md
from flask_jwt_extended import get_jwt_identity
from app.jwt import locksmith_required, user_required
from sqlalchemy import and_

bp_service = Blueprint('service', __name__)

@bp_service.route('/get-service-list', methods=['GET'])
@locksmith_required
def service_list():
    _filter = and_(md.active == True, md.locksmith_id == get_jwt_identity())
    return ma(many=True).jsonify(md.query.filter(_filter).all()), 200

@bp_service.route('/add-service', methods=['POST'])
@locksmith_required
def add_service():
    request.json['locksmith_id'] = get_jwt_identity()
    value = ma().load(request.json)
    current_app.db.session.add(value)
    current_app.db.session.commit()
    return jsonify({'msg': 'sucess'}), 201

@bp_service.route('/update-service', methods=['POST'])
@locksmith_required
def update_service():
    request.json['locksmith_id'] = get_jwt_identity()
    _filter = and_(md.locksmith_id == get_jwt_identity(), md.id == request.json['id'])
    result = md.query.filter(_filter).first()
    service = ma().dump(result)
    if service:
        md.query.filter(_filter).update(request.json)
        current_app.db.session.commit()
        return jsonify({'msg': 'sucess'}), 201
    else:
        return jsonify({'msg': 'Failed'}), 409

@bp_service.route('/delete-service', methods=['POST'])
@locksmith_required
def delete_service():
    _filter = and_(md.locksmith_id == get_jwt_identity(), md.id == request.json['id'])
    result = md.query.filter(_filter).first()
    service = ma().dump(result)
    if service:
        md.query.filter(_filter).update({"active": False})
        current_app.db.session.commit()
        return jsonify({'msg': 'sucess'}), 201
    else:
        return jsonify({'msg': 'Failed'}), 409
        