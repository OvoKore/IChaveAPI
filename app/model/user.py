from app.model import db
from flask import current_app
from sqlalchemy import Column, Integer, String, DateTime, Date, exists
from passlib.hash import pbkdf2_sha512
from datetime import datetime

class User(db.Model):
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)
    cell_phone = Column(String(20), nullable=False, unique=True)
    cpf = Column(String(11), nullable=False, unique=True)
    sex = Column(String(10), nullable=False)
    birthdate = Column(Date(), nullable=False)

    def gen_hash(self):
        self.password = pbkdf2_sha512.hash(self.password)

    def verify_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)

    def verify_unique_key(self, user):
        email = current_app.db.session.query(exists().where(User.email == user.email)).scalar()
        cell_phone = current_app.db.session.query(exists().where(User.cell_phone == user.cell_phone)).scalar()
        cpf = current_app.db.session.query(exists().where(User.cpf == user.cpf)).scalar()
        if email or cell_phone or cpf:
            msg = ''
            if email:
                msg += "Email\n"
            if cell_phone:
                msg += "Cell Phone's Number\n"
            if cpf:
                msg += "CPF\n"
            return "Are Already in Use:\n" + msg
        return None
