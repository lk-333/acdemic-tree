from database import Database
from typing import List
import hashlib
import time
from typing import Dict

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
        
            
   

    
        
