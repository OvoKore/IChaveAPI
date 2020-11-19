from app.serializer import ma
from app.model.user import User as md

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = md
        load_instance = True