from flask import Flask, jsonify,request
from typing import List, Dict
import numpy as np

app = Flask(__name__)

class Node:
    def __init__(self, user_id=None):
        self.user_id: int = user_id
        self.mentees: List[List[Node, int]] = []
        self.mentors: List[List[Node, int]] = []

atree={}

def find_msg(s):
    return [1, 2, 3, 4, "Real Name", "http://profile.link"]

def locate_nodes(me_node: Node):
    nodes=[]
    links=[]
    
    def recursion(ments:List[List[Node, int]],x,y,flag,depth,fa_name):
        N=len(ments)
        if N%2==1:
            x_lst=np.array(range(-int((N-1)/2),int((N+1)/2)+1)*100)
        else:
            x_lst=np.array(range(-(int(N/2)),int(N/2)))*100+50
            
        if flag==1:
            y_now=y-100
        else:
            y_now=y+100 
            
        for x_now,node_now in zip(x_lst,ments):
            node_now=node_now[0]
            tmp_node_dic={}
            s=find_msg(node_now.user_id)
            tmp_node_dic["real_name"]=s[4]
            tmp_node_dic["user_id"]=node_now.user_id
            tmp_node_dic["x"]=x_now
            tmp_node_dic["y"]=y_now
            nodes.append(tmp_node_dic)
            
            tmp_link_dic={}
            if flag==1:
                tmp_link_dic["source"]=s[4]
                tmp_link_dic["target"]=fa_name
            else:
                tmp_link_dic["source"]=fa_name
                tmp_link_dic["target"]=s[4]
            links.append(tmp_link_dic)
                
            if depth>0:
                if flag==1:
                    recursion(node_now.mentors,x_now,y_now,flag,depth-1)
                else:
                    recursion(node_now.mentees,x_now,y_now,flag,depth-1)
                       
    me_x=500
    me_y=300
    me_dic = {}
    s = find_msg(me_node.user_id)
    me_dic["real_name"] = s[4]
    me_dic["user_id"] = me_node.user_id
    me_dic["profile_link"] = s[5]
    me_dic["x"]=me_x
    me_dic["y"]=me_y
    nodes.append(me_dic)
    
    recursion(me_node.mentors,me_x,me_y,1,1,me_dic["real_name"])
    recursion(me_node.mentees,me_x,me_y,0,1,me_dic["real_name"])
    
    data={}
    data["ndoes"]=nodes
    data["links"]=links
    return data

    
    

@app.route('/bulid_tree')
def bulid_tree():
    data=request.get_json()
    x_me=500
    y_me=300
    
    tree=locate_nodes(atree[data["id"]])
    return jsonify(tree)
if __name__ == '__main__':
    app.run(debug=True)
