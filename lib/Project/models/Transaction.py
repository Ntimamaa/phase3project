from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))

    user = relationship('User', back_populates='transactions')
    book = relationship('Book', back_populates='transactions')
