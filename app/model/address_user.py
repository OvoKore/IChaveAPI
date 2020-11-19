from app.model import db
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class AddressUser(db.Model):
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    main = Column(Boolean)
    name = Column(String(20))
    cep = Column(String(9), nullable=False)
    uf = Column(String(2), nullable=False)
    cidade = Column(String(50), nullable=False)
    bairro = Column(String(100), nullable=False)
    logradouro = Column(String(100), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(50))
    active = Column(Boolean(), default=True)