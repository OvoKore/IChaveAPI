from flask import Blueprint, request, jsonify, current_app
from app.serializer.address_user import AddressUserSchema as ma
from app.model.address_user import AddressUser as md
from app.jwt import user_required, user_required
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import and_

bp_address_user = Blueprint('address_user', __name__)

@bp_address_user.route('/get-address-list', methods=['GET'])
@user_required
def user_address_list():
    _filter = and_(md.active == True, md.user_id == get_jwt_identity())
    return ma(many=True).jsonify(md.query.filter(_filter).all()), 200

@bp_address_user.route('/add-address', methods=['POST'])
@user_required
def add_user_address():
    request.json['user_id'] = get_jwt_identity()
    value = ma().load(request.json)
    if value.main:
        _filter = and_(md.user_id == get_jwt_identity())
        md.query.filter(_filter).update({"main": False})
        current_app.db.session.commit()
    current_app.db.session.add(value)
    current_app.db.session.commit()
    return jsonify({'msg': 'sucess'}), 201

@bp_address_user.route('/update-address', methods=['POST'])
@user_required
def update_user_address():
    request.json['user_id'] = get_jwt_identity()
    _filter = and_(md.user_id == get_jwt_identity(), md.id == request.json['id'])
    result = md.query.filter(_filter).first()
    address = ma().dump(result)
    if address:
        if address['main']:
            tmp_filter = md.user_id == get_jwt_identity()
            md.query.filter(tmp_filter).update({"main": False})
        md.query.filter(_filter).update(request.json)
        current_app.db.session.commit()
        return jsonify({'msg': 'sucess'}), 201
    else:
        return jsonify({'msg': 'Failed'}), 409

@bp_address_user.route('/delete-address', methods=['POST'])
@user_required
def delete_user_address():
    _filter = and_(md.user_id == get_jwt_identity(), md.id == request.json['id'])
    result = md.query.filter(_filter).first()
    address = ma().dump(result)
    if address:
        md.query.filter(_filter).update({"active": False})
        current_app.db.session.commit()
        return jsonify({'msg': 'sucess'}), 201
    else:
        return jsonify({'msg': 'Failed'}), 409