from database import Database
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import queue
import time
from args import args
from DataStruct import AcdemicTree,Node
from typing import List
import numpy as np
    
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

@app.route("/update-profile",methods=['POST'])
def update_profile():
    data=request.get_json()
    status,s=atree.update_personal_info(username = data['username'], realName = data['realName'], homepage = data['homepage'])
    return jsonify({'status':status})


@app.route("/search_user",methods=['POST'])
def search_user():
    data=request.get_json()
    status=atree.check_username_exists(username = data['name'])
    return jsonify({'status':status})

@app.route('/bulid_tree',methods=['POST'])
def bulid_tree():
    data=request.get_json()
    user_node=atree.users[int(data['id'])]
    tree=atree.locate_nodes(user_node)
    return jsonify(tree)

if __name__=="__main__":   
    app.run(debug=True)
    
    