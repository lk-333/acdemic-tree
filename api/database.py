import pymysql
import hashlib
import time
import threading
from args import args
from typing import Dict

max_id=1000

class Database():
    def __init__(self):
        self.db=pymysql.connect(
            # 主机名
            host=args["db_host"],
            # 端口
            port=int(args["db_port"]),
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


    def get_rel_info(self, mentorship_id: int) -> Dict[str, str]:
        query = f"SELECT mentorship_id, mentor_id, mentee_id, start_date, end_date FROM mentorship WHERE mentorship_id = {mentorship_id}"
        result = self.exec(query)
        if not result:
            return {}

        mentorship = result[0]
        mentorship_data = {
            "mentorship_id": mentorship[0],
            "mentor_id": mentorship[1],
            "mentee_id": mentorship[2],
            "start_time": mentorship[3].strftime("%Y-%m-%d"),
            "end_time": mentorship[4].strftime("%Y-%m-%d") if mentorship[4] else None
        }
        return mentorship_data

    def register(self, user_id, user_name, password, identity, institute):
        self.exec(f"""
            INSERT INTO user (user_id, user_name, password, identity, institute)
            VALUES ({user_id}, '{user_name}', '{password}', '{identity}', '{institute}')
        """)
    
    def add_user_msg(self,real_name,profile_link):
        self.exec(f"""
                    insert
                    into user (real_name,profile_link)
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
        
    def insert_application_data(self, applicant_name, respondent_name, creation_time):
        # Check if applicant_name and respondent_name exist in user table
        applicant_check = self.exec(f"SELECT COUNT(*) FROM user WHERE user_name = '{applicant_name}'")
        respondent_check = self.exec(f"SELECT COUNT(*) FROM user WHERE user_name = '{respondent_name}'")

        if int(applicant_check[0][0]) > 0 and int(respondent_check[0][0]) > 0:
            self.exec(f"""
                INSERT INTO application (applicant_name, respondent_name, creation_time, is_processed, process_result)
                VALUES ('{applicant_name}', '{respondent_name}', '{creation_time}', FALSE, '')
            """)
            return 0, f"Inserted application for applicant_name {applicant_name} and respondent_name {respondent_name} successfully."
        else:
            return 1, f"Error: applicant_name {applicant_name} or respondent_name {respondent_name} does not exist in user table."

    #根据id查询user表中的一列信息
    def get_user_info(self, user_id):
        user_info = self.exec(f"""
            SELECT * FROM user WHERE user_id = {user_id}
        """)
        if user_info:
            return user_info[0]
        else:
            return f"Error: User with user_id {user_id} does not exist."

