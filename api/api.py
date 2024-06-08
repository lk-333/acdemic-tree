from database import Database
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import queue
import time

# to_pre_queue = queue.Queue() 
# from_pre_quque = queue.Queue()  
    





def back():
    while True:
        time.sleep(1000)

def run_back_thread():
    th=threading.Thread(target=back,)
    th.start()
    return th

app = Flask(__name__)
db=Database()

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    print(f"前端发给我的数据:{data}")
    num1 = data['num1']
    num2 = data['num2']
    sum_result = num1 + num2
    return jsonify({'sum': sum_result,'sum2':2})

@app.route('/check_user',methods=['POST'])
def check_user():
    data=request.get_json()
    status=db.check_user(user_name=data["username"],password=data['password'],identity=data['identity'])
    return jsonify({'status':status})

@app.route("register_user",methods=['POST']) 
def register_user():
    data=request.get_json()
    status=db.add_user(user_name=data["username"],password=data['password'],identity=data['identity'])
    return jsonify({'status':status})
    
    
if __name__=="__main__":   
    def run():
        app.run(debug=True)
    
    run()
    back_thread=run_back_thread()
    
    