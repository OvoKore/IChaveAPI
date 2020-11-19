from app.serializer import ma
from marshmallow import fields, validates, ValidationError, validates_schema
from app.model.address_locksmith import AddressLochsmith as md

class AddressLocksmithSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = md
        include_fk = True
        load_instance = True