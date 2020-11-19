from flask import Blueprint, request, jsonify, current_app
from app.serializer.locksmith import LocksmithSchema as ma
from app.model.locksmith import Locksmith as md
from flask_jwt_extended import get_jwt_identity
from app.jwt import locksmith_required
from app.util import decrypt
from sqlalchemy import and_, or_
import json

bp_locksmith = Blueprint('locksmith', __name__)

@bp_locksmith.route('/get-user-locksmith', methods=['GET'])
@locksmith_required
def show():
    _filter = md.id == get_jwt_identity()
    result = md.query.filter(_filter).first()
    resp = json.loads(ma(many=False).dumps(result))
    del resp['password']
    del resp['id']
    return jsonify(resp), 200

@bp_locksmith.route('/create-user-locksmith', methods=['POST'])
def register():
    if request.json.get('state_registration') is None:
        del request.json['state_registration']
    request.json['password'] = decrypt(request.json.get('password'))

    locksmith = ma().load(request.json)
    verify = locksmith.verify_unique_key()
    if verify is not None:
        return jsonify({'msg': verify}), 409

    locksmith.gen_hash()
    current_app.db.session.add(locksmith)
    current_app.db.session.commit()

    return jsonify({'msg': 'sucess'}), 201

@bp_locksmith.route('/update-user-locksmith', methods=['POST'])
@locksmith_required
def update():
    del request.json['password']
    request.json['id'] = get_jwt_identity()
    u = request.json
    _filter = (
        and_(md.id != u['id'], 
            or_(md.company_name == u['company_name'], 
                or_(md.cell_phone == u['cell_phone'], 
                    or_ (md.email == u['email'], md.cnpj == u['cnpj'])
    ))))
    search = md.query.filter(_filter).all()
    if not search:
        tmp_filter = md.id == u['id']
        md.query.filter(tmp_filter).update(u)
        current_app.db.session.commit()
        return jsonify({'msg': 'sucess'}), 200
    else:
        return jsonify({'msg': 'Some information already has changed already appears in our records.'}), 200

@bp_locksmith.route('/change-user-locksmith-password', methods=['POST'])
@locksmith_required
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
    
@bp_locksmith.route('/get-status-locksmith', methods=['GET'])
@locksmith_required
def get_status():
    _filter = md.id == get_jwt_identity()
    result = md.query.filter(_filter).first()
    resp = json.loads(ma(many=False).dumps(result))
    return jsonify(resp['status']), 200

@bp_locksmith.route('/change-status-locksmith', methods=['POST'])
@locksmith_required
def change_status():
    _filter = md.id == get_jwt_identity()
    result = md.query.filter(_filter).first()
    resp = json.loads(ma(many=False).dumps(result))
    md.query.filter(_filter).update({'status': not resp['status']})
    current_app.db.session.commit()
    return jsonify(not resp['status']), 200