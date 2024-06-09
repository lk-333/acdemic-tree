import pymysql
import threading
from args import args


class Database():
    def __init__(self):
        self.db = pymysql.connect(
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

    def alter_application_table(self):
        # 添加 is_processed 列
        # self.exec("""
        #     ALTER TABLE application
        #     ADD COLUMN is_processed BOOLEAN DEFAULT FALSE
        # """)

        # 添加 process_result 列，没有默认值
        self.exec("""
            ALTER TABLE application
            ADD COLUMN process_result TEXT
        """)

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


# 实例化数据库类
db = Database()

# 修改现有的 application 表
db.alter_application_table()

# 插入数据（确保 user 表中有对应的 user_name）
result, message = db.insert_application_data('StuLiMing', '品爷', '2024-06-09 12:11:00')
print(result, message)

result, message = db.insert_application_data('齐天大圣', '李明', '2024-06-09 13:00:00')
print(result, message)
