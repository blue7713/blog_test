from flask import Flask, jsonify, request, make_response, session # status상태를 넘겨주기 위한 make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
import os 
from blog_control.user_mgmt import User
from blog_view import blog

# https 만을 지원하는 기능을 http 에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static') # html을 가져올 폴더는 static임을 명시

CORS(app)
# script태그안의 타 사이트의 url을 사용할 수 있도록 함
app.secret_key = 'my_server1'
# app.secret_key = os.urandom(24) # 보안을 위해 서버를 켤 때 랜덤한 키를 생성
# 이 경우 서버를 다시 켜면 기존의 session 정보(동일한 사용자들 정보)는 재사용 불가

app.register_blueprint(blog.blog_abtest, url_prefix='/blog') # blueprint 등록
login_manager = LoginManager() # loginManager 객체 생성
login_manager.init_app(app)
login_manager.session_protection = 'strong' # 보안을 높일수록 session을 복잡하게 구현 가능

@login_manager.user_loader # mysql에서 user_id를 리턴해주는 매서드
def load_user(user_id): # http request에서 id를 추출하여 자동으로 할당
    return User.get(user_id)

@login_manager.unauthorized_handler # 로그인이 안된 사용자가 로그인이 된 사용자만이 접속할 수 있는 사이트를 요청하면 보여주는 페이지설정
def unauthorized():
    return make_response(jsonify(success=False), 401) # 허용되지 않는 페이지임을 리턴

@app.before_request
def app_before_requset():
    if 'client_id' not in session: # http의 모든 요청에 대한 정보는 session에 있음
        session['client_id'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        # 만약 session에 정보가 없다면 실제 데이터를 가진 서버 주소를 sseioon[client_id]라는 dic에 저장
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True )
