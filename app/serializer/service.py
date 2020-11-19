from app.serializer import ma
from marshmallow import fields, validates, ValidationError, validates_schema
from app.model.service import Service as md

class ServiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = md
        include_fk = True
        load_instance = True