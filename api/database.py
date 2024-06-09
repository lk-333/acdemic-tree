import pymysql
import hashlib
import time
import threading
from args import args

max_id=1000

class Database():
    def __init__(self):
        self.db=pymysql.connect(
            # 主机名
            host=args["db_host"],
            # 端口
            port=args["db_port"],
            # 用户名
            user=args["db_user"],
            # 密码
            password=args["db_password"],
            # 数据库
            database=args['db_database'],
            # 自动 commit
            autocommit=True)
        self.cursor = self.db.cursor()
        self.lock = threading.Lock()  # 创建一个锁实例
    
    def exec(self,order:str):
        with self.lock: 
            try:
                
                self.cursor.execute(order)
                results = self.cursor.fetchall()
            except Exception as e:
                print("Database process error")
                print(e)
                return tuple(())
            return results


    
    def register(self,user_id,user_name,password,identity):
        self.exec(f"""
                    insert
                    into person (user_id,user_name,password)
                    values ({user_id},'{user_name}','{password}','{identity}')
                """)
    
    def add_user_msg(self,real_name,profile_link):
        self.exec(f"""
                    insert
                    into person (real_name,profile_link)
                    values ('{real_name}','{profile_link}',)
                  """)
        
    def add_mentorship(self,mentorship_id,mentor_id,mentee_id,start_date=None,end_date=None):
        self.exec(f"""
                    insert 
                    into mentorship
                    values ({mentorship_id},{mentor_id},{mentee_id},'{start_date}','{end_date}')
                    """)
    
    def del_mentorship(self,mentor_id,mentee_id):
        self.exec(f"""
                delete
                from mentorship
                where mentor_id={mentor_id} and mentee_id={mentee_id}
                """) 
    
    def del_person(self):
        pass
    
    
    # -1:用户不存在
    # 0：密码错误
    # 1：密码正确
    def check_user(self,user_name,password,identity):
        user_exist=self.exec(f"""
                  SELECT COUNT(*) FROM user WHERE user_name = '{user_name}' AND identity='{identity}'
                  """)
        user_exist=int(user_exist[0][0])
        if user_exist==0:
            return -1
        
        password_right=self.exec(f"""
                                 SELECT COUNT(*) FROM user WHERE user_name = '{user_name}' AND password='{password}' AND identity='{identity}'
                                 """)
        password_right=int(password_right[0][0])
        if password_right==1:
            return 1
        elif password_right==0:
            return 0
        
    
