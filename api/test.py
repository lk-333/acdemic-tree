import pymysql
import random
from args import args

# 随机生成机构名称的函数
def get_random_institute():
    institutes = ["Institute A", "Institute B", "Institute C", "Institute D", "Institute E"]
    return random.choice(institutes)

# 数据库连接设置
db = pymysql.connect(
    host=args["db_host"],
    port=int(args["db_port"]),
    user=args["db_user"],
    password=args["db_password"],
    database=args['db_database'],
    autocommit=True
)

cursor = db.cursor()

# 向 user 表中添加 institute 列
try:
    cursor.execute("ALTER TABLE user ADD COLUMN institute VARCHAR(255)")
    print("Column 'institute' added successfully.")
except Exception as e:
    print(f"Error adding column 'institute': {e}")

# 获取所有用户
cursor.execute("SELECT user_id FROM user")
users = cursor.fetchall()

# 为每个用户随机分配一个 institute 值
for user in users:
    user_id = user[0]
    institute = get_random_institute()
    cursor.execute(f"UPDATE user SET institute = '{institute}' WHERE user_id = {user_id}")

print("All users updated with random institute values.")

# 关闭数据库连接
cursor.close()
db.close()
