import db_auth as db_auth
import pymysql.cursors

class MenuRepository:
    def __init__(self) -> None:
        self.login = db_auth.db_login

    def getConnection(self):
        self.connection = pymysql.connect(host=self.login['host'],
                                     user=self.login['user'],
                                     password=self.login['password'],
                                     db=self.login['db'],
                                     charset=self.login['charset'],
                                     cursorclass=pymysql.cursors.DictCursor)

    def closeConnection(self):
        self.connection.close()

        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        dinner_sql = "INSERT INTO menudata (menu) VALUES ('%s')" % (menuData)
        cursor.execute(dinner_sql) # 쿼리 실행 
        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제

        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체
        
        sql = "UPDATE menudata SET score='%s', reviewcount='%s' WHERE menu='%s'" % (score, reviewCount, menu)   
        print(sql)     
        cursor.execute(sql)
        self.connection.commit() # 쿼리 적용
        result = cursor.fetchone()

        self.closeConnection()
        return result