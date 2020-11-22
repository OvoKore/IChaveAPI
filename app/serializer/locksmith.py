from app.serializer import ma
from app.model.locksmith import Locksmith as md

class LocksmithSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = md
        load_instance = True