import configparser

# 创建一个配置解析器对象
config = configparser.ConfigParser()

# 读取配置文件
config.read('config.conf')

args={}
args["db_user"]=config.get('Database', 'db_user')
args["db_password"]=config.get('Database', 'db_password')