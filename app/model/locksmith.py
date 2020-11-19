from app.model import db
from flask import current_app
from sqlalchemy import Column, Integer, String, DateTime, Boolean, exists, and_
from passlib.hash import pbkdf2_sha512
from datetime import datetime

class Locksmith(db.Model):

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    cell_phone = Column(String(20), nullable=False, unique=True)
    cnpj = Column(String(14), nullable=False, unique=True)
    company_name = Column(String(50), nullable=False, unique=True)
    state_registration = Column(String(50), nullable=True, unique=True)
    status = Column(Boolean(), default=False)

    def gen_hash(self):
        self.password = pbkdf2_sha512.hash(self.password)

    def verify_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)

    def verify_unique_key(self):
        email = current_app.db.session.query(exists().where(Locksmith.email == self.email)).scalar()
        cell_phone = current_app.db.session.query(exists().where(Locksmith.cell_phone == self.cell_phone)).scalar()
        company_name = current_app.db.session.query(exists().where(Locksmith.company_name == self.company_name)).scalar()
        cnpj = current_app.db.session.query(exists().where(Locksmith.cnpj == self.cnpj)).scalar()
        state_registration = current_app.db.session.query(exists().where(and_(Locksmith.state_registration == self.state_registration, Locksmith.state_registration != None))).scalar()
        if email or cell_phone or company_name or cnpj:
            msg = ''
            if email:
                msg += "Email\n"
            if cell_phone:
                msg += "Cell Phone's Number\n"
            if company_name:
                msg += "Company's Name\n"
            if cnpj:
                msg += "CNPJ\n"
            if state_registration:
                msg += "State Registration\n"
            return "Are Already in Use:\n" + msg
        return None
