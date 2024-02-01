import pymysql

MYSQL_HOST = 'localhost'
MYSQL_CONN = pymysql.connect(
    host = MYSQL_HOST,
    port = 3306,
    user = 'root',
    passwd = '@Ks24764056',
    db = 'blog_db',
    charset = 'utf8'
    )

def conn_mysql(): # 연결이 끊어져 있을 경우 사용 함수
    if not MYSQL_CONN.open:
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN