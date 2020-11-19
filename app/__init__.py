from flask import Flask
from flask_migrate import Migrate
from app.model import configure as config_db
from app.serializer import configure as config_ma
from app.jwt import configure as config_jwt
from app.util import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY, decrypt

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = decrypt(SQLALCHEMY_DATABASE_URI)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = decrypt(JWT_SECRET_KEY)
    app.config['JWT_IDENTITY_CLAIM'] = 'sub'

    config_db(app)
    config_ma(app)

    Migrate(app, app.db)

    config_jwt(app)

    from .route import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
