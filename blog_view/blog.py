from flask import Flask, Blueprint, request, render_template, jsonify, make_response, redirect, url_for, session
from blog_control.user_mgmt import User
from flask_login import login_user, current_user, logout_user
from datetime import timedelta
from blog_control.session_mgmt import BlogSession

blog_abtest = Blueprint('blog', __name__)

@blog_abtest.route('/set_email', methods=['GET', 'POST']) # html에서 데이터를 받음, get방식은 url에 정보 표시, post 방식은 url에 정보 표시x
def set_email():
    if request.method == 'GET':
        print('get_email', request.args.get('user_email'))
        return redirect(url_for('blog.blog_fullstack1')) # 다른 라우팅 경로 반환, url_for은 blueprint의 이름을 이용
        # return redirect('/blog/test_blog') # 다른 라우팅 경로 반환, 전체 url경로를 써주어야 함
        # return make_response(jsonify(success=True), 200) # jsoin으로 데이터만 전달
    else: # POST 방식
        # print('post_email', request.form['user_email']) # html에서 form을 사용할 경우 body의 정보를 가져오려면 request.form을 사용
        # print('set_email', request.get_json()) 
        # get_json은 content type이 application/json 인 경우 body를 가져올 수 있음\
        user = User.create(request.form['user_email'], 'A') # html의 form태그에서의 user_email 정보를 가져와 db에 새로 만듬
        login_user(user, remember=True, duration=timedelta(days=365)) # user 정보를 바탕으로 세션을 만듬
        # 365일동안 로그인 정보 기억
        return redirect(url_for('blog.blog_fullstack1'))
    
@blog_abtest.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user() # 로그아웃을 해주는 flask 모듈
    return redirect(url_for('blog.blog_fullstack1'))
    
@blog_abtest.route('/blog_fullstack1')
def blog_fullstack1():
    if current_user.is_authenticated: # 현재 유저가 로그인되어 있는지 확인(abtest의 user_loader 함수를 호출하여 확인하는 구조)
        webpage_name = BlogSession.get_blog_page(current_user.blog_id)
        BlogSession.save_session_info(session['client_id'], current_user.user_email, webpage_name)
        return render_template(webpage_name, user_email=current_user.user_email) # 해당 주소를 입력하면 보여줄 페이지 리턴, 로그인 되어 있다면 해당 이메일을 보여주는 페이지 리턴
    else:
        webpage_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(session['client_id'], 'anonymous', webpage_name) # 로그인이 안되어 있으므로 아무나 저장하라는 anonymous
        return render_template(webpage_name) # 로그인이 안되어 있다면 기존 페이지 리턴