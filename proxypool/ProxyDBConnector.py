import pymysql
import datetime


class ProxyDB:

    def __init__(self, password, **kwd):

        self._user = kwd.get('user', 'root')
        self._pwd = password

        self.connect()
        

    def connect(self):

        self.db = pymysql.connect(user = self._user,
                                  password = self._pwd,
                                  database = 'proxydb')
        self.cursor = self.db.cursor()


    def insert(self, proxy, source=None):

        sql = """INSERT INTO proxyPool
                 VALUES('{proxy}', '{checktime}', '{expiretime}', '{source}')"""

        checktime = datetime.datetime.now()
        expiretime = checktime + datetime.timedelta(days = 1)  # hard to change
        checktime = checktime.strftime('%Y-%m-%d %H:%M:%S')
        expiretime = expiretime.strftime('%Y-%m-%d %H:%M:%S')

        if source is None: source = 'NULL'

        self.cursor.execute(sql.format(proxy = proxy,
                                       checktime = checktime,
                                       expiretime = expiretime,
                                       source = source))

        self.db.commit()
