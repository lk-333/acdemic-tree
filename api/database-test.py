import pymysql
import threading
from args import args


class Database():
    def __init__(self):
        self.db = pymysql.connect(
            # 主机名
            host='192.168.250.147',
            # 端口
            port=3306,
            # 用户名
            user=args["db_user"],
            # 密码
            password=args["db_password"],
            # 数据库
            database='academic_rel_tree',
            # 自动 commit
            autocommit=True
        )
        self.cursor = self.db.cursor()
        self.lock = threading.Lock()  # 创建一个锁实例

    def exec(self, order: str):
        with self.lock:
            try:
                self.cursor.execute(order)
                results = self.cursor.fetchall()
            except Exception as e:
                print("Database process error")
                print(e)
                return tuple(())
            return results

    def create_application_table(self):
        self.exec("""
            CREATE TABLE IF NOT EXISTS application (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                applicant_id BIGINT,
                respondent_id BIGINT,
                creation_time DATETIME,
                FOREIGN KEY (applicant_id) REFERENCES user(user_id),
                FOREIGN KEY (respondent_id) REFERENCES user(user_id)
            )
        """)

    def insert_application_data(self, applicant_id, respondent_id, creation_time):
        # Check if applicant_id and respondent_id exist in user table
        applicant_check = self.exec(f"SELECT COUNT(*) FROM user WHERE user_id = {applicant_id}")
        respondent_check = self.exec(f"SELECT COUNT(*) FROM user WHERE user_id = {respondent_id}")

        if int(applicant_check[0][0]) > 0 and int(respondent_check[0][0]) > 0:
            self.exec(f"""
                INSERT INTO application (applicant_id, respondent_id, creation_time)
                VALUES ({applicant_id}, {respondent_id}, '{creation_time}')
            """)
            print(
                f"Inserted application for applicant_id {applicant_id} and respondent_id {respondent_id} successfully.")
        else:
            print(f"Error: applicant_id {applicant_id} or respondent_id {respondent_id} does not exist in user table.")


# 实例化数据库类
db = Database()

# 创建 application 表
db.create_application_table()

# 插入数据（确保 user 表中有对应的 user_id）
db.insert_application_data(111, 222, '2024-06-09 12:00:00')
db.insert_application_data(222, 333, '2024-06-09 12:30:00')
db.insert_application_data(111, 333, '2024-06-09 13:00:00')

print("Table 'application' created and data inserted successfully.")
