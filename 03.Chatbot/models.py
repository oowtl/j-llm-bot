# python DB = SQLAlchemy
# pip install sqlalchemy

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# table structure
class Items(Base):
  __tablename__ = 'items'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  price = Column(Integer)
  stock = Column(Integer)
  created_at = Column(DateTime)
  
  
class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, autoincrement=True)
  email = Column(String)
  name = Column(String)
  phone = Column(String)
  created_at= Column(DateTime)
  
  # 사용자가 구매한 구매이력들에 대한 참조가 가능하다.
  purchase = relationship('Purchase', back_populates='user')
  # 역참조(ORM 방식) => 부모도 자녀를 찾을 수 있도록 하는 것
  # 1 : N 관계에서 1 인 곳에서 N을 참조할 수 있도록 한다.
  
class Purchase(Base):
  __tablename__ = 'purchases'
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
  quality = Column(Integer)
  status = Column(String)
  purchase_date= Column(DateTime) 
  
  user = relationship("User", back_populates='purchase')
  # back_populates 에는 class 의 속성명으로 설정해준다.
  item = relationship("Items")