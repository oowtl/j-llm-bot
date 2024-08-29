from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

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
    messages=[
      {
        "role": "user",
        "content" : user_input
      }
    ]
  )
  
  return res.choices[0].message.content

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    user_input = request.form['user_input']
    
    bot_response = make_prompt(user_input=user_input)
    
    messages.append({"role": "user", "text": user_input})
    messages.append({"role": "bot", "text" : bot_response})
        
  return render_template('index.html', messages=messages)

if __name__ == "__main__":
  app.run(debug=True)