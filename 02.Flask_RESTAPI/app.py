from flask import Flask
from routes import register_routes

app = Flask(__name__)
register_routes(app)

@app.route('/')
def index():
  return {"Hello" : "Flask!"}

# 간단한 API 만들기
@app.route('/api/v1/feeds', methods=['GET']) # REST API [GET] /api/v1/feeds
def show_all_feeds():
    data = {'result' : 'success', 'data' : {'feed1': 'data1', 'feed2': 'data2'}}
    # 데이터 타입 : 파이썬 Dict=> 브라우저가 이해할 수 없다.
    
    return data # jsonify


@app.route('/api/v1/feeds<int:feed_id>', methods=['GET']) # REST API [GET] /api/v1/feeds
def show_one_feed(feed_id):
  data = {'result': 'sucess', 'data': f'feed ID : {feed_id}'}
  return data

@app.route('/api/v1/feeds', methods = ['POST'])
def create_feed():
  email = request.form['email']
  content = request.form['content']
  data = {'result': 'sucess', 'data': {'email':email, 'content':content}}
  
  return data

if __name__ == '__main__':
  app.run()
  # 마이크로서비스 아키텍처 : 기능 하나당 서버 하나. -> 하나가 터져도 다른 기능은 문제가 없다.
  