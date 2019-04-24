import pymysql.cursors
import datetime


class mysql(object):
    def __init__(self, mysql_config):
        self.host = mysql_config['host']
        self.user = mysql_config['user']
        self.password = mysql_config['password']
        self.db = mysql_config['db']

        self.charset = 'utf8mb4'
        self.cursorclass = pymysql.cursors.DictCursor
        self.ssl = {'ca': '/xxx/xxx/xxx.pem'}

        self.connect = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            charset=self.charset,
            cursorclass=self.cursorclass)

    def query_data(self, username):
        date = datetime.datetime.now().strftime("%Y%m%d")
        start = date + '000000'
        end = date + '173000'
        with self.connect.cursor() as cursor:
            sql = "SELECT COUNT(p.id) AS access_count FROM idm_audit_data AS p WHERE p.username = %s AND p.operate_time BETWEEN %s AND %s"
            cursor.execute(sql, (username, start, end))
            result = cursor.fetchone()
            return result


if __name__ == '__main__':
    conn = {
        'host': '192.168.100.81',
        'user': 'root',
        'password': 'password',
        'db': 'idb'
    }

    m = mysql(conn)
    result = m.query_data("xinhe")
    print(result['access_count'])
