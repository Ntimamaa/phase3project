from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .Base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    transactions = relationship('Transaction', back_populates='user')
