from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine)
SessionLocal = sessionmaker(autocommit=False, bind=engine)
# autocommit : db.commit() 을 하지 않아도 commit 을 해준다.
# autoflush : db 에 데이터를 보내는 것

# db 시작
def init_db():
  Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  
  # yield 를 사용해서 db 연결을 끊고 맺는 것을 할 수 있도록 한다.
  try:
    yield db
  except:
    db.close()
    
init_db()