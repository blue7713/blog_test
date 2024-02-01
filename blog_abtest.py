from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
# script태그안의 타 사이트의 url을 사용할 수 있도록 함
app.secret_key = 'my_server1'
# app.secret_key = os.urandom(24) # 보안을 위해 서버를 켤 때 랜덤한 키를 생성
# 이 경우 서버를 다시 켜면 기존의 session 정보(동일한 사용자들 정보)는 재사용 불가

app.register_blueprint(blog.blog_abtest, url_prefix = '/blog')