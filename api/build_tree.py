from flask import Flask, jsonify
from typing import List,Dict

app = Flask(__name__)

class Node:
    def __init__(self,user_id=None):
        self.user_id:int=user_id
        # Node+mentorship_id
        self.mentees:List[List[Node,int]]=[]
        self.mentors:List[List[Node,int]]=[]
        
users:Dict[int,Node]={}

def find_msg(s):
    return [1,2,3,4]

def locate_nodes(me_node:Node):
    nodes=[]
    me_dic={}
    s=find_msg(me_node.user_id)
    me_dic["real_name"]=s[4]
    me_dic["profile_link"]=s[5]
    
    
    
    
@app.route('/deliver_tree')
def deliver_tree():
    data = {
        "nodes": [    
            { "id": "Professor A", "x": 700, "y": 250,"profile_link":"www.bilibili.com" },
            { "id": "Professor B", "x": 600, "y": 350 },
            { "id": "Professor C", "x": 800, "y": 350 },
            { "id": "Professor D", "x": 700, "y": 450 },
            { "id": "Professor E", "x": 600, "y": 550 },
            { "id": "Professor F", "x": 800, "y": 550 },
            { "id": "Professor G", "x": 900, "y": 600 }
        ],
        "links": [
            { "source": "Professor A", "target": "Professor B" },
            { "source": "Professor A", "target": "Professor C" },
            { "source": "Professor B", "target": "Professor D" },
            { "source": "Professor C", "target": "Professor D" },
            { "source": "Professor C", "target": "Professor E" },
            { "source": "Professor D", "target": "Professor F" },
            { "source": "Professor G", "target": "Professor D" }
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
