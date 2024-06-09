from database import Database
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import queue
import time
from args import args
from DataStruct import AcdemicTree

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
atree=AcdemicTree(db=db)


@app.route('/check_user',methods=['POST'])
def check_user():
    data=request.get_json()
    status=db.check_user(user_name=data["username"],password=data['password'],identity=data['identity'])
    return jsonify({'status':status})

@app.route("/register_user",methods=['POST']) 
def register_user():
    data=request.get_json()
    status=atree.register(user_name=data["username"],password=data['password'],identity=data['identity'])
    return jsonify({'status':status})

@app.route("/send-application",methods=['POST'])
def send_application():
    data=request.get_json()
    status,s=atree.apply_for_mentorship(applicant_name=data["yourName"],respondent_name=data['otherName'])
    return jsonify({'status':status})

    
if __name__=="__main__":   
    def run():
        app.run(debug=True)
    
    run()
    back_thread=run_back_thread()
    
    