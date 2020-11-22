from app.model import db
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey

class Service(db.Model):
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    low_price = Column(Float(6.2), nullable=False)
    high_price = Column(Float(6.2), nullable=False)
    locksmith_id = Column(Integer, ForeignKey('locksmith.id'))
    active = Column(Boolean(), default=True)