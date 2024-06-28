from database import Database
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import queue
import time
from args import args
from DataStruct import AcdemicTree, Node
from typing import List
import numpy as np


treeView_dict={}
tree_id=0
class TreeView():
    def __init__(self,node:Node):
        data=self.build_tree(node)
        self.nodes=data["nodes"]
        self.links=data["links"]

    def build_tree(self,me_node: Node):
        nodes = []
        links = []

        def recursion(ments, x, y, flag, depth, fa_name):
            N = len(ments)
            if N % 2 == 1:
                x_lst = np.array(range(-int((N - 1) / 2), int((N + 1) / 2) + 1) )* (100+depth*150)
            else:
                x_lst = np.array(range(-(int(N / 2)), int(N / 2))) * (100+depth*150) + 50

            if flag == 1:
                y_now = y - 100
            else:
                y_now = y + 100

            for x_now, ment in zip(x_lst, ments):
                node_now,link_now = ment
                tmp_node_dic = {}
                s = db.get_user_info(node_now.user_id)
                tmp_node_dic["real_name"] = s[4]
                tmp_node_dic["user_id"] = node_now.user_id
                tmp_node_dic["x"] = int(x)+int(x_now)
                tmp_node_dic["y"] = int(y_now)
                nodes.append(tmp_node_dic)

                tmp_link_dic = {}
                if flag == 1:
                    tmp_link_dic["source"] = s[4]
                    tmp_link_dic["target"] = fa_name
                else:
                    tmp_link_dic["source"] = fa_name
                    tmp_link_dic["target"] = s[4]
                now_rel=db.get_rel_info(link_now)
                tmp_link_dic["start_time"]=now_rel["start_time"]
                tmp_link_dic["end_time"]=now_rel["end_time"]
                links.append(tmp_link_dic)

                if depth > 0:
                    if flag == 1:
                        if len(node_now.mentors)>1:
                            recursion(node_now.mentors, tmp_node_dic["x"], tmp_node_dic["y"], flag, depth - 1, tmp_node_dic["real_name"])
                    else:
                        if len(node_now.mentees)>1:
                            recursion(node_now.mentees, tmp_node_dic["x"], tmp_node_dic["y"], flag, depth - 1, tmp_node_dic["real_name"])

        me_x = 500
        me_y = 300
        me_dic = {}
        s = db.get_user_info(me_node.user_id)
        me_dic["real_name"] = s[4]
        me_dic["user_id"] = me_node.user_id
        me_dic["profile_link"] = s[5]
        me_dic["x"] = me_x
        me_dic["y"] = me_y
        nodes.append(me_dic)

        recursion(me_node.mentors, me_x, me_y, 1, 1, me_dic["real_name"])
        recursion(me_node.mentees, me_x, me_y, 0, 1, me_dic["real_name"])

        data = {}
        data["nodes"] = nodes
        data["links"] = links
        return data

    
    def send(self):
        data={}
        data["nodes"]=self.nodes
        data["links"]=self.links
        return data

    def refresh(self):
        pass





app = Flask(__name__)
CORS(app)
db = Database()
atree = AcdemicTree(db=db)


@app.route('/api/check_user', methods=['POST'])
def check_user():
    data = request.get_json()
    status = db.check_user(user_name=data["username"], password=data['password'], identity=data['identity'])
    return jsonify({'status': status})


@app.route("/api/register_user", methods=['POST'])
def register_user():
    data = request.get_json()
    status = atree.register(user_name=data["username"], password=data['password'], identity=data['identity'])
    return jsonify({'status': status})


@app.route("/api/send-application", methods=['POST'])
def send_application():
    data = request.get_json()
    status, s = atree.apply_for_mentorship(applicant_name=data["yourName"], respondent_name=data['otherName'])
    return jsonify({'status': status})


@app.route("/api/update-profile", methods=['POST'])
def update_profile():
    data = request.get_json()
    status, s = atree.update_personal_info(username=data['username'], realName=data['realName'],
                                           homepage=data['homepage'])
    return jsonify({'status': status})


@app.route("/api/search_user", methods=['POST'])
def search_user():
    data = request.get_json()
    status = atree.check_username_exists(username=data['name'])
    return jsonify({'status': status})


@app.route("/api/get-applications", methods=['POST'])
def get_applications():
    data = request.get_json()
    s = atree.get_processed_applications(username=data['username'])
    return jsonify({'applications': s})


@app.route("/api/deal-applications", methods=['POST'])
def deal_applications():
    data = request.get_json()
    status, s = atree.process_application(item_id=data['item_id'], result=data['result'])
    print(data['item_id'])
    print(data['result'])
    return jsonify({'status': status})


@app.route('/api/bulid_tree', methods=['POST'])
def bulid_tree():
    global tree_id
    data = request.get_json()
    user_node = atree.users[int(data['id'])]
    tree_view=TreeView(user_node)
    tree_id+=1
    treeView_dict[tree_id]=tree_view
    print(tree_view.send())
    return jsonify(tree_view.send())

@app.route('/api/refreshTreeView',methods=['POST'])
def refressTreeView():
    data = request.get_json()
    treeView_dict[data["tree_id"]].refresh()
    
@app.route("/api/get-Allapplications", methods=['POST'])
def get_Allapplications():
    data = request.get_json()
    s = atree.get_Allapplications()
    return jsonify({'applications': s})

@app.route("/api/fsearch_user", methods=['POST'])
def fserch_user():
    data = request.get_json()

    s = atree.search_user(data['name'],data['type'])
    print(s)
    return jsonify({'results': s})

@app.route("/api/userAvailability", methods=['POST'])
def userAvailability():
    data = request.get_json()

    s = atree.check_user_exists(data['username'])
    print(s)
    return jsonify({'isAvailable': s})

if __name__ == "__main__":
    def run():
        app.run(debug=True)

    run()

