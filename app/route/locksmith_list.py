
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from app.jwt import user_required
from sqlalchemy import and_
import json
from app.model.address_user import AddressUser
from app.serializer.address_user import AddressUserSchema
from app.model.locksmith import Locksmith
from app.serializer.locksmith import LocksmithSchema
from app.model.address_locksmith import AddressLochsmith
from app.serializer.address_locksmith import AddressLocksmithSchema
from app.serializer.service import ServiceSchema
from app.model.service import Service

bp_locksmith_list = Blueprint('locksmith_list', __name__)

@bp_locksmith_list.route('/get-locksmith-list', methods=['GET'])
@user_required
def get_locksmith_list():
    _filter = and_(
        AddressUser.user_id == get_jwt_identity(),
        AddressUser.main == True,
        AddressUser.active == True
    )
    result = AddressUser.query.filter(_filter).first()
    if result:
        my_address = json.loads(AddressUserSchema(many=False).dumps(result))
        _filter = and_(
            AddressLochsmith.uf == my_address['uf'],
            AddressLochsmith.cidade == my_address['cidade'],
            AddressLochsmith.active == True,
            AddressLochsmith.main == True,
            AddressLochsmith.locksmith_id == Locksmith.id,
            Locksmith.status == True
        )
        result = current_app.db.session.query(
            AddressLochsmith.locksmith_id,
            AddressLochsmith.cep,
            AddressLochsmith.uf,
            AddressLochsmith.cidade,
            AddressLochsmith.bairro,
            AddressLochsmith.logradouro,
            AddressLochsmith.numero,
            AddressLochsmith.complemento,
            Locksmith.company_name,
            Locksmith.cell_phone
        ).filter(_filter).all()
        response = list()
        for r in result:
            response.append({
                "locksmith_id": r.locksmith_id,
                "company_name": r.company_name,
                "cep": r.cep,
                "uf": r.uf,
                "cidade": r.cidade,
                "bairro": r.bairro,
                "logradouro": r.logradouro,
                "numero": r.numero,
                "complemento": r.complemento,
                "cell_phone": r.cell_phone
            })
        return jsonify(response), 200
    return jsonify(list()), 200

@bp_locksmith_list.route('/get-locksmith-services', methods=['GET'])
@user_required
def get_locksmith_services():
    _filter = and_(Service.active == True, Service.locksmith_id == request.json)
    return ServiceSchema(many=True).jsonify(Service.query.filter(_filter).all()), 200