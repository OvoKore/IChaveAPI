from app.serializer import ma
from marshmallow import fields, validates, ValidationError, validates_schema
from app.model.address_user import AddressUser as md

class AddressUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = md
        include_fk = True
        load_instance = True