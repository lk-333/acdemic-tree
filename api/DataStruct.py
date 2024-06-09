from database import Database
from typing import List
import hashlib
import time
from typing import Dict,Tuple
import numpy as np
import json

max_id=1000

class Node:
    def __init__(self,user_id=None):
        self.user_id:int=user_id
        # Node+mentorship_id
        self.mentees:List[List[Node,int]]=[]
        self.mentors:List[List[Node,int]]=[]
            
class AcdemicTree():
    def __init__(self,db:Database):
        self.db=db
        
        db_users=db.exec("""
                select * from user
                """)
        db_mentorships=db.exec(
            """
            select * from mentorship
            """
        )
        
        self.users:Dict[int,Node]={}
        for user in db_users:
            user_node=Node(user[0])
            self.users[user[0]]=user_node
        
        for r in db_mentorships:
            mentorship_id=r[0]
            mentor_id=r[1]
            mentee_id=r[2]
            self.users[mentee_id].mentors.append([self.users[mentor_id],mentorship_id])
            self.users[mentor_id].mentees.append([self.users[mentee_id],mentorship_id])
    
    # 0 用户名已存在
    # 1 注册成功             
    def register(self,user_name,password,identity):
        user_id=int(hashlib.sha256((user_name+password+identity).encode()).hexdigest(),16)%int(max_id)
        if self.users.get(user_id):
            return 0
        newguy=Node(user_id=user_id)
        self.users[user_id]=newguy
        self.db.register(user_id=user_id,user_name=user_name,password=password,identity=identity)
        return 1
    
        
    def add_mentorship(self,mentor_id,mentee_id,start_date=None,end_date=None):
        if start_date==None:
            start_date=time.strftime("%Y-%m-%d",time.gmtime())
        if end_date==None:
            end_date="1970-01-01"
        mentorship_id=(mentee_id+mentee_id)%int(max_id)
        self.users[mentee_id].mentors.append([self.users[mentor_id],mentorship_id])
        self.users[mentor_id].mentees.append([self.users[mentee_id],mentorship_id])
        self.db.add_mentorship(mentorship_id,mentor_id,mentee_id,start_date,end_date)
    
    def del_mentorship(self,mentor_id,mentee_id):
        mentors_origin=self.users[mentee_id].mentors
        mentors_new=[]
        for mentor in mentors_origin:
            if mentor[0].user_id!=mentor_id:
                mentors_new.append(mentor)
        self.users[mentee_id].mentors=mentors_new
        
        mentees_origin=self.users[mentor_id].mentees
        mentees_new=[]
        for mentee in mentees_origin:
            if mentee[0].user_id!=mentee_id:
                mentees_new.append(mentee)
        self.users[mentor_id].mentees=mentees_new
        self.db.del_mentorship(mentor_id,mentee_id)
        
    def del_person(self):
        pass
   
    # TODO:to be modified
    def check_relationship(self,real_name):
        def id2msg2json(user_id):
            db_ret=self.db.exec(f"""
                     select from user 
                     where real_name='{real_name}'
                     """)
            real_name=db_ret[0][4]
            profile_link=db_ret[0][5]
            js={
                "name":real_name,
                "attributes": {
                "link": profile_link
                },
            }
            return js
        
        db_ret=self.db.exec(f"""
                     select from user 
                     where real_name='{real_name}'
                     """)
        me_id=db_ret[0][0]
        me_js=id2msg2json(me_id)
        me_js["children"]=[id2msg2json(mentee[0].user_id for mentee in self.users[me_id].mentees)]
        return me_js

    # 处理申请
    # 如果申请成功，则返回0，并在数据库中添加一个申请条目
    # 如果申请失败，则返回1，并返回报错信息
    def apply_for_mentorship(self, applicant_name, respondent_name, creation_time=None) -> Tuple[int, str]:
        # 检查申请的合法性
        if applicant_name == respondent_name:
            return 0, f"Error: applicant_name {applicant_name} and respondent_name {respondent_name} cannot be the same."

        applicant_check = self.db.exec(f"SELECT COUNT(*) FROM user WHERE user_name = '{applicant_name}'")
        respondent_check = self.db.exec(f"SELECT COUNT(*) FROM user WHERE user_name = '{respondent_name}'")

        if int(applicant_check[0][0]) == 0:
            return 0, f"Error: applicant_name {applicant_name} does not exist."

        if int(respondent_check[0][0]) == 0:
            return 0, f"Error: respondent_name {respondent_name} does not exist."

        if creation_time is None:
            creation_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        self.db.insert_application_data(applicant_name, respondent_name, creation_time)
        return 1, f"Application submitted successfully for applicant_name {applicant_name} and respondent_name {respondent_name}."

    # 修改个人信息
    def update_personal_info(self, username: str, realName: str, homepage: str) -> Tuple[int, str]:
        user_check = self.db.exec(f"SELECT COUNT(*) FROM user WHERE user_name = '{username}'")

        if int(user_check[0][0]) == 0:
            return 0, f"Error: username {username} does not exist."

        self.db.exec(f"""
            UPDATE user 
            SET real_name = '{realName}', profile_link = '{homepage}'
            WHERE user_name = '{username}'
        """)
        return 1, f"User {username} information updated successfully."

    def check_username_exists(self, username: str) -> int:
        user_check = self.db.exec(f"SELECT COUNT(*) FROM user WHERE real_name = '{username}'")
        if int(user_check[0][0]) > 0:
            return 1
        else:
            return 0
    # 查询未处理的申请条目
    def get_processed_applications(self, username: str) -> List[Dict[str, str]]:
        processed_apps = self.db.exec(f"""
            SELECT applicant_name, item_id, creation_time FROM application 
            WHERE respondent_name = '{username}' AND is_processed = FALSE
        """)
        results = []
        for app in processed_apps:
            result = {
                "applicantName": app[0],
                "applicantTime": app[2].strftime("%Y-%m-%d %H:%M:%S"),# 将 datetime 转换为字符串
                "item_id": app[1]
            }
            results.append(result)
        return results

    def locate_nodes(self,me_node:Node):
        nodes=[]
        links=[]
        
        def recursion(ments,x,y,flag,depth,fa_name):
            N=len(ments)
            if N%2==1:
                x_lst=x+np.array(range(-int((N-1)/2),int((N+1)/2)+1))*100
            else:
                x_lst=x+np.array(range(-(int(N/2)),int(N/2)))*100+50
                
            if flag==1:
                y_now=y-100
            else:
                y_now=y+100 
                
            for x_now,node_now in zip(x_lst,ments):
                node_now=node_now[0]
                tmp_node_dic={}
                s=self.db.get_user_info(node_now.user_id)
                tmp_node_dic["real_name"]=s[4]
                tmp_node_dic["user_id"]=node_now.user_id
                tmp_node_dic["x"]=int(x_now)
                tmp_node_dic["y"]=int(y_now)
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
                        recursion(node_now.mentors,x_now,y_now,flag,depth-1,tmp_node_dic["real_name"])
                    else:
                        recursion(node_now.mentees,x_now,y_now,flag,depth-1,tmp_node_dic["real_name"])
                        
        me_x=500
        me_y=300
        me_dic = {}
        s = self.db.get_user_info(me_node.user_id)
        me_dic["real_name"] = s[4]
        me_dic["user_id"] = me_node.user_id
        me_dic["profile_link"] = s[5]
        me_dic["x"]=me_x
        me_dic["y"]=me_y
        nodes.append(me_dic)
        
        recursion(me_node.mentors,me_x,me_y,1,1,me_dic["real_name"])
        recursion(me_node.mentees,me_x,me_y,0,1,me_dic["real_name"])
        
        data={}
        data["nodes"]=nodes
        data["links"]=links
        return data


    
# 实例化数据库类
db = Database()

# 创建 AcdemicTree 实例
academic_tree = AcdemicTree(db)

# 测试获取处理完成的申请条目
processed_applications = academic_tree.get_processed_applications('品爷')
print(json.dumps(processed_applications, indent=2, ensure_ascii=False))
