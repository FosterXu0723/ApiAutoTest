# 作者       ：yangwuxie
# 创建时间   ：2020/8/12 15:23
import pymysql

from common.ReadConfig import ReadConfig


def mysql_db():
    conn = pymysql.connect(
        host=ReadConfig.db_host,
        port=int(ReadConfig.db_port),
        user=ReadConfig.db_username,
        password=ReadConfig.db_password,
        db=ReadConfig.db_name
    )
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT token from rhino_agent_token where agent_id in (SELECT id from rhino_agent where username="17602116237") ORDER BY create_time DESC'
            cursor.execute(sql)
            fetchall = cursor.fetchone()
            print(fetchall)
            print(type(fetchall))
    finally:
        cursor.close()


mysql_db()
