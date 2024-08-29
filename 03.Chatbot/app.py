from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

from database import get_db
from sqlalchemy import text

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
modelName = os.getenv("OPENAI_MODEL_NAME")

client = OpenAI(api_key=api_key)

# 메세지 한번에 보이도록 하기 위해서 사용하는 리스트
# 챗봇의 내용은 6개월 동안 보관을 해야한다.(법적인 요구사항)
messages = []

# 웹서버
# Nginx (리버스 프록시)
# (1) 로드 밸런서 => 트래픽 분산
# (2) 보안 => 다이렉트로 자바 서버로 접근하게 되면 보안이 취약해진다.
# 포워드 프록시
# 지리적으로 너무 멀리있는 곳에 서버를 제공하기 위해서 정적 파일을 그 지역에 가져다 놓는 것으로 속도를 높인다.
# Java Spring Nginx Architecture
# Nginx + docker

def make_prompt (user_input):
  res = client.chat.completions.create(
    model=modelName,
    messages=user_input
  )
  
  return res.choices[0].message.content

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
  db = next(get_db())
  if request.method == 'POST':
    user_input = request.form['user_input']
    

    # 이 부분은 설계를 해야한다.
    if '구매내역' in user_input:
      # name, email = extract_customer_name_email(user_input) # 회원인지 아닌지 확인해야한다.
      # query = f"SELECT * FROM users WHERE name={user}"
      
      name = 'JunHong'
      email = 'ooooo@gmail.com'
      query = text("SELECT * FROM users WHERE name = :name AND email = :email")
      user = db.execute(query, {"name" : name, "email": email}).fetchone()
      
      if user:
        # bot_response = f"안녕하세요! 쇼픵 봇 이에요!"  
        query = text('SELECT * FROM purchases WHERE user_id = :user_id')
        purchases = db.execute(query, {'user_id': user[0]}).fetchall()
          
        if purchases:
          purchase_detail = "\n".join(
            f"주문 ID : {p[0]}, {p[3]}, {p[4]}" for p in purchases
          )
          
          bot_response = f"{user[2]} 님의 주문 내역은 다음과 같습니다. {purchase_detail}"
        else:
          bot_response = '주문 내역이 확인되지 않습니다.'
      else:
        bot_response = '회원정보가 확인되지 않습니다.'
        
    elif '환불요청' in user_input:
      name, email = extract_customer_name_email(user_input) # 회원인지 아닌지 확인해야한다.
      # query = f"SELECT * FROM users WHERE name={user}"
      query = text("SELECT * FROM users WHERE name = :user AND email = :email")
      user = db.execute(query, {"name" : name}).fetchone()
      
      if user:
        # bot_response = f"안녕하세요! 쇼픵 봇 이에요!"
        
        query = text('SELECT * FROM purchase WHERE user_id = :user_id')
        purchases = db.execute(query, {'user_id': user['id']}).fetchall()
          
        if purchases:
          purchase_detail = "\n".join(
            f"주문 ID : {p[0]}, {p[3]}, {p[4]}" for p in purchases
          )
          
          bot_response = f"{user[2]} 님의 주문 내역은 다음과 같습니다. {purchase_detail}"
        else:
          bot_response = '주문 내역이 확인되지 않습니다.'
      else:
        bot_response = '회원정보가 확인되지 않습니다.'
    else:
      # prompt 작성
      conversation = [
        {
          "role" : "system",
          "content" : "You are a very kindful and helpful shopping mall C/S assistant"
        }
      ]
      conversation.extend([
        {
          "role" : msg['role'],
          "content" : msg['content']
        } for msg in messages
      ])
      conversation.append(
        {
          "role" : "user",
          "content": user_input
        }
      )
    
      bot_response = make_prompt(user_input=conversation)
      
    messages.append({
      'role': 'user',
      'content': user_input
    })
    messages.append({
      'role': 'assistant',
      'content': bot_response
    })
      
  return render_template('index.html', messages=messages)

import re
def extract_customer_name_email(input_text):
  # 정규 표현식을 사용해서 이름과 이메일을 추출한다.
  
  # 이름:박준홍, 이메일 : junhong@gmail.com
  name_pattern = r"[가-힣][가-힣]*"
  email_pattern = r"[a-zA-Z0-9]+@+[a-zA-Z0-9]+\.[a-zA-Z]{2,}"
  
  name_match = re.search(name_pattern, input_text)
  email_match = re.search(email_pattern, input_text)
  
  name = name_match.group(0) if name_match else None
  email = email_match.group(0) if (email_match) else None
  
  # return name, email
  return ('JunHong', email)

if __name__ == "__main__":
  app.run(debug=True)
  


# DB 연결
# sqlite 로 코드 구조를 잡고 mysql (서버) 로 변경 - 호스트 주소, 포트 등..