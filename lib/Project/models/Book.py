from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.Base import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    is_available = Column(Boolean, default=True)

    transactions = relationship('Transaction', back_populates='book')
