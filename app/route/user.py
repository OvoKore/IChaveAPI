from flask import Blueprint, request, jsonify, current_app
from app.serializer.user import UserSchema as ma
from app.model.user import User as md
from flask_jwt_extended import get_jwt_claims, get_jwt_identity
from app.jwt import user_required
from app.util import decrypt
from sqlalchemy import and_, or_
from dateutil.parser import parse
import json

bp_user = Blueprint('user', __name__)

@bp_user.route('/get-user', methods=['GET'])
@user_required
def show():
    _filter = md.id == get_jwt_identity()
    result = md.query.filter(_filter).first()
    resp = json.loads(ma(many=False).dumps(result))
    del resp['password']
    del resp['id']
    return jsonify(resp), 200

@bp_user.route('/create-user', methods=['POST'])
def register():
    request.json['password'] = decrypt(request.json.get('password'))
    request.json['birthdate'] = parse(request.json['birthdate']).date().strftime('%Y-%m-%d')

    user = ma().load(request.json)
    verify = user.verify_unique_key(user)
    if verify is not None:
        return jsonify({'msg': verify}), 409

    user.gen_hash()
    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify({'msg': 'sucess'}), 201

@bp_user.route('/update-user', methods=['POST'])
@user_required
def update():
    del request.json['password']
    request.json['id'] = get_jwt_identity()
    u = request.json
    _filter = (
        and_(md.id != u['id'], 
            or_(md.cell_phone == u['cell_phone'], 
                or_ (md.email == u['email'], md.cpf == u['cpf'])
    )))
    search = md.query.filter(_filter).all()
    if not search:
        tmp_filter = md.id == u['id']
        md.query.filter(tmp_filter).update(u)
        current_app.db.session.commit()
        return jsonify({'msg': 'sucess'}), 200
    else:
        return jsonify({'msg': 'Some information already has changed already appears in our records.'}), 200

@bp_user.route('/change-user-password', methods=['POST'])
@user_required
def change_password():
    old_password = decrypt(request.json['old_password'])
    new_password = decrypt(request.json['new_password'])
    _filter = md.id == get_jwt_identity()
    result = md.query.filter(_filter).first()
    user = json.loads(ma(many=False).dumps(result))
    u = md()
    u.password = user['password']
    if u.verify_password(old_password):
        u.password = new_password
        u.gen_hash()
        md.query.filter(_filter).update({'password': u.password})
        current_app.db.session.commit()
        return jsonify({'msg': 'sucess'}), 201
    else:
        return jsonify({'msg': 'Wrong current password'}), 201
