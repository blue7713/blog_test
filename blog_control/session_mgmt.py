from db_model.mysql import conn_mysql
from datetime import datetime

class BlogSession():
    blog_page = {'A' : 'blog_A.html', 'B' : 'blog_B.html'}
    session_count = 0
    
    @staticmethod
    def save_session_info(session_ip, user_email, webpage_name): # 접속 정보 저장 매서드
        now = datetime.now()
        now_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        mysql_db = conn_mysql()
        db_cursor = mysql_db.cursor()
        sql = "INSERT INTO session_info (session_ip, user_email, page, access_time) \
        VALUES (%s, %s, %s, %s)"
        db_cursor.execute(sql, (session_ip, user_email, webpage_name, now_time))
        mysql_db.commit()
        
    @staticmethod
    def get_blog_page(blog_id=None): # 인자를 주지 않으면 force = 0, force값에 따라 페이지 할당
        # 임의의 사용자의 경우 50:50으로 A, B 페이지를 보여줌
        # 구독한 페이지가 있다면 force에 할당하여 그 페이지를 리턴
        if blog_id == None:
            if BlogSession.session_count == 0:
                BlogSession.session_count = 1
                return BlogSession.blog_page['A']
            else:
                BlogSession.session_count = 0
                return BlogSession.blog_page['B']
        else:
            return BlogSession.blog_page[blog_id]
        