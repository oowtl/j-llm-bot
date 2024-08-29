from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, User, Purchase, Items

# ORM 방식으로 데이터를 처리해주는데 MYSQL 로도 가능하다.

engine = create_engine("sqlite:///test.db")
# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# 예제 데이터 추가
item1 = Items(name="삼성 노트북", price = 10000, stock = 10, created_at = datetime.now())
item2 = Items(name="LG 노트북", price = 20000, stock = 10, created_at = datetime.now())
item3 = Items(name="맥북 에어", price = 30000, stock = 10, created_at = datetime.now())
item4 = Items(name="맥북 프로 13", price = 40000, stock = 10, created_at = datetime.now())
item5 = Items(name="맥북 프로 16", price = 50000, stock = 10, created_at = datetime.now())

session.add_all([item1, item2, item3, item4, item5])
session.commit()

user1 = User(name ='JunHong', email = 'ooooo@gmail.com', phone='01033334444', created_at = datetime.now())
user2 = User(name ='JunHong', email = 'ooooo@gmail.com', phone='01033334444', created_at = datetime.now())

session.add_all([user1, user2])
session.commit()

purchase1 = Purchase(user_id = user1.id, item_id = item4.id, quality = 1, status='paid', purchase_date = datetime.now())
purchase2 = Purchase(user_id = user1.id, item_id = item5.id, quality = 1, status='cancled', purchase_date = datetime.now())

session.add_all([purchase1, purchase2])
session.commit()


# 챗봇 LLM
# 1. 비용이 아직까지 비싸다.
# 2. 보안 문제가 있다. (유저 데이터를 LLN에게 넘겨줘야한다.)
# 3. 가스라이팅을 통해서 고객 데이터를 알아낼 수 있다.