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


# to_pre_queue = queue.Queue()
# from_pre_quque = queue.Queue()  

def locate_nodes(me_node: Node):
    nodes = []
    links = []

    def recursion(ments: List[List[Node, int]], x, y, flag, depth, fa_name):
        N = len(ments)
        if N % 2 == 1:
            x_lst = np.array(range(-int((N - 1) / 2), int((N + 1) / 2) + 1) * 100)
        else:
            x_lst = np.array(range(-(int(N / 2)), int(N / 2))) * 100 + 50

        if flag == 1:
            y_now = y - 100
        else:
            y_now = y + 100

        for x_now, node_now in zip(x_lst, ments):
            node_now = node_now[0]
            tmp_node_dic = {}
            s = db.get_user_info(node_now.user_id)
            tmp_node_dic["real_name"] = s[4]
            tmp_node_dic["user_id"] = node_now.user_id
            tmp_node_dic["x"] = x_now
            tmp_node_dic["y"] = y_now
            nodes.append(tmp_node_dic)

            tmp_link_dic = {}
            if flag == 1:
                tmp_link_dic["source"] = s[4]
                tmp_link_dic["target"] = fa_name
            else:
                tmp_link_dic["source"] = fa_name
                tmp_link_dic["target"] = s[4]
            links.append(tmp_link_dic)

            if depth > 0:
                if flag == 1:
                    recursion(node_now.mentors, x_now, y_now, flag, depth - 1)
                else:
                    recursion(node_now.mentees, x_now, y_now, flag, depth - 1)

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
    data["ndoes"] = nodes
    data["links"] = links
    return data


def back():
    while True:
        time.sleep(1000)


def run_back_thread():
    th = threading.Thread(target=back, )
    th.start()
    return th


app = Flask(__name__)
db = Database()
atree = AcdemicTree(db=db)


@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.get_json()
    status = db.check_user(user_name=data["username"], password=data['password'], identity=data['identity'])
    return jsonify({'status': status})


@app.route("/register_user", methods=['POST'])
def register_user():
    data = request.get_json()
    status = atree.register(user_name=data["username"], password=data['password'], identity=data['identity'])
    return jsonify({'status': status})


@app.route("/send-application", methods=['POST'])
def send_application():
    data = request.get_json()
    status, s = atree.apply_for_mentorship(applicant_name=data["yourName"], respondent_name=data['otherName'])
    return jsonify({'status': status})


@app.route("/update-profile", methods=['POST'])
def update_profile():
    data = request.get_json()
    status, s = atree.update_personal_info(username=data['username'], realName=data['realName'],
                                           homepage=data['homepage'])
    return jsonify({'status': status})


@app.route("/search_user", methods=['POST'])
def search_user():
    data = request.get_json()
    status = atree.check_username_exists(username=data['name'])
    return jsonify({'status': status})


@app.route("/get-applications", methods=['POST'])
def get_applications():
    data = request.get_json()
    s = atree.get_processed_applications(username=data['username'])
    return jsonify({'applications': s})


@app.route("/deal-applications", methods=['POST'])
def deal_applications():
    data = request.get_json()
    status, s = atree.process_application(item_id=data['item_id'], result=data['result'])
    print(data['item_id'])
    print(data['result'])
    return jsonify({'status': status})


@app.route('/bulid_tree', methods=['POST'])
def bulid_tree():
    data = request.get_json()
    user_node = atree.users[int(data['id'])]
    tree = atree.locate_nodes(user_node)
    return jsonify(tree)


@app.route("/get-Allapplications", methods=['POST'])
def get_Allapplications():
    data = request.get_json()
    s = atree.get_Allapplications()
    return jsonify({'applications': s})

@app.route("/fserch_user", methods=['POST'])
def fserch_user():
    data = request.get_json()
    s = atree.search_user(data['name'],data['searchType'])
    return jsonify({'applications': s})


if __name__ == "__main__":
    def run():
        app.run(debug=True)


    run()
    back_thread = run_back_thread()

