# python DB = SQLAlchemy
# pip install sqlalchemy

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# table structure
class Items(Base):
  __tablename__ = 'items'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  price = Column(Integer)
  stock = Column(Integer)
  created_at = Column(DateTime)
  