from flask_login import UserMixin
from db_model.mysql import conn_mysql

class User(UserMixin):
    
    def __init__ (self, user_id, user_email, blog_id):
        self.user_id = user_id
        self.user_email = user_email
        self.blog_id = blog_id
        
    def get_id(self):
        return str(self.id) # 유니코드로 나타내주기 위해 str로 변환
    
    @staticmethod
    def get(user_id):
        