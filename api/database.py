import pymysql
import hashlib
import time

max_id=1000

class Database():
    def __init__(self):
        self.db=pymysql.connect(
            # 主机名
            host='localhost',
            # 端口
            port=3306,
            # 用户名
            user='root',
            # 密码
            password='123456',
            # 数据库
            database='academic_rel_tree',
            # 自动 commit
            autocommit=True)
        self.cursor = self.db.cursor()
    
    def exec(self,order:str):
        try:
            self.cursor.execute(order)
            results = self.cursor.fetchall()
        except Exception as e:
            print("Database process error")
            print(e)
            return tuple(())
        return results

    def add_person(self,name,profile):
        person_id=int(hashlib.sha256((name+profile).encode()).hexdigest(),16)%int(max_id)
        self.exec(f"""
                    insert
                    into person
                    values ({person_id},'{name}','{profile}')
                  """)
    
    def add_mentorship(self,mentor_id,mentee_id,start_date=None,end_date=None):
            if start_date==None:
                start_date=time.strftime("%Y-%m-%d",time.gmtime())
            if end_date==None:
                end_date="1970-01-01"
            mentorship_id=(mentee_id+mentee_id)%int(max_id)
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
    
    def add_user(self,user_name,password,identity):
        self.exec(f"""
                    insert 
                    into user
                    values ('{user_name}','{password}','{identity}')
                    """)
    
    # -1:用户不存在
    # 0：密码错误
    # 1：密码正确
    def check_user(self,user_name,password,identity):
        user_exist=self.exec(f"""
                  SELECT COUNT(*) FROM user WHERE user_name = '{user_name}' AND identity='{identity}'
                  """)
        if user_exist==0:
            return -1
        password_right=self.exec(f"""
                                 SELECT COUNT(*) FROM user WHERE user_name = '{user_name}' AND password='{password}' AND identity='{identity}'
                                 """)
        if password_right==1:
            return 1
        elif password_right==0:
            return 0
        
    
