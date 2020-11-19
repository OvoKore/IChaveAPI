from flask import Blueprint, request, jsonify, current_app
from app.serializer.address_locksmith import AddressLocksmithSchema as ma
from app.model.address_locksmith import AddressLochsmith as md
from app.jwt import locksmith_required, user_required
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import and_

bp_address_locksmith = Blueprint('address_locksmith', __name__)

@bp_address_locksmith.route('/get-locksmith-address-list', methods=['GET'])
@locksmith_required
def locksmith_address_list():
    _filter = and_(md.active == True, md.locksmith_id == get_jwt_identity())
    return ma(many=True).jsonify(md.query.filter(_filter).all()), 200

@bp_address_locksmith.route('/add-locksmith-address', methods=['POST'])
@locksmith_required
def add_locksmith_address():
    request.json['locksmith_id'] = get_jwt_identity()
    value = ma().load(request.json)
    if value.main:
        _filter = and_(md.locksmith_id == get_jwt_identity())
        md.query.filter(_filter).update({"main": False})
        current_app.db.session.commit()
    current_app.db.session.add(value)
    current_app.db.session.commit()
    return jsonify({'msg': 'sucess'}), 201

@bp_address_locksmith.route('/update-locksmith-address', methods=['POST'])
@locksmith_required
def update_locksmith_address():
    request.json['locksmith_id'] = get_jwt_identity()
    _filter = and_(md.locksmith_id == get_jwt_identity(), md.id == request.json['id'])
    result = md.query.filter(_filter).first()
    address = ma().dump(result)
    if address:
        tmp_filter = md.locksmith_id == get_jwt_identity()
        md.query.filter(tmp_filter).update({"main": False})
        md.query.filter(_filter).update(request.json)
        current_app.db.session.commit()
        return jsonify({'msg': 'sucess'}), 201
    else:
        return jsonify({'msg': 'Failed'}), 409

@bp_address_locksmith.route('/delete-locksmith-address', methods=['POST'])
@locksmith_required
def delete_locksmith_address():
    _filter = and_(md.locksmith_id == get_jwt_identity(), md.id == request.json['id'])
    result = md.query.filter(_filter).first()
    address = ma().dump(result)
    if address:
        md.query.filter(_filter).update({"active": False})
        current_app.db.session.commit()
        return jsonify({'msg': 'sucess'}), 201
    else:
        return jsonify({'msg': 'Failed'}), 409