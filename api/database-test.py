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
        # Ensure the user_name column in user table has an index
        index_check = self.exec("SHOW INDEX FROM user WHERE Key_name='idx_user_name'")
        if not index_check:
            self.exec("CREATE INDEX idx_user_name ON user(user_name)")

        # Create the application table
        self.exec("""
            CREATE TABLE IF NOT EXISTS application (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                applicant_name VARCHAR(255),
                respondent_name VARCHAR(255),
                creation_time DATETIME,
                FOREIGN KEY (applicant_name) REFERENCES user(user_name),
                FOREIGN KEY (respondent_name) REFERENCES user(user_name)
            )
        """)

    def insert_application_data(self, applicant_name, respondent_name, creation_time):
        # Check if applicant_name and respondent_name exist in user table
        applicant_check = self.exec(f"SELECT COUNT(*) FROM user WHERE user_name = '{applicant_name}'")
        respondent_check = self.exec(f"SELECT COUNT(*) FROM user WHERE user_name = '{respondent_name}'")

        if int(applicant_check[0][0]) > 0 and int(respondent_check[0][0]) > 0:
            self.exec(f"""
                INSERT INTO application (applicant_name, respondent_name, creation_time)
                VALUES ('{applicant_name}', '{respondent_name}', '{creation_time}')
            """)
            return 0, f"Inserted application for applicant_name {applicant_name} and respondent_name {respondent_name} successfully."
        else:
            return 1, f"Error: applicant_name {applicant_name} or respondent_name {respondent_name} does not exist in user table."


# 实例化数据库类
db = Database()

# 创建新的 application 表
db.create_application_table()

# 插入数据（确保 user 表中有对应的 user_name）
result, message = db.insert_application_data('StuLiMing', '品爷', '2024-06-09 12:11:00')
print(result, message)

result, message = db.insert_application_data('齐天大圣', '李明', '2024-06-09 13:00:00')
print(result, message)
