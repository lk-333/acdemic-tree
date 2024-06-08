from database import Database
from typing import List
import hashlib
import time
from typing import Dict

max_id=1000

class Node:
    def __init__(self,person_id=None,name=None,profile_link=None) -> None:
        self.person_id:int=person_id
        self.name:str=name
        self.profile_link:str=profile_link
        self.childs:List[List[Node,str,str]]=[]
        self.mentor:Node=Node
            
class AcdemicTree():
    def __init__(self,db:Database):
        self.db=db
        
        db_persons=db.exec("""
                select * from person
                """)
        db_mentorships=db.exec(
            """
            select * from mentorship
            """
        )
        
        self.persons:Dict[int,Node]={}
        for p in db_persons:
            person_id=p[0]
            name=p[1]
            profile_link=p[2]
            p_node=Node(person_id,name,profile_link)
            self.persons[person_id]=p_node
        
        for r in db_mentorships:
            mentorship_id=r[0]
            mentor_id=r[1]
            mentee_id=r[2]
            start_date=r[3]
            end_date=r[4]
            self.persons[mentee_id].mentor=self.persons[mentor_id]
            self.persons[mentor_id].childs.append([self.persons[mentee_id],start_date,end_date])
                    
    def add_person(self,name,profile_link):
        person_id=int(hashlib.sha256((name+profile_link).encode()).hexdigest(),16)%int(max_id)
        newguy=Node(person_id=person_id,name=name,profile_link=profile_link)
        self.persons[person_id]=newguy
        self.db.add_person(name=name,profile=profile_link)
    
    def add_mentorship(self,mentor_id,mentee_id,start_date=None,end_date=None):
        if start_date==None:
            start_date=time.strftime("%Y-%m-%d",time.gmtime())
        if end_date==None:
            end_date="1970-01-01"
        self.persons[mentee_id].mentor=self.persons[mentor_id]
        self.persons[mentor_id].childs.append([self.persons[mentee_id],start_date,end_date])
        self.db.add_mentorship(mentor_id,mentee_id,start_date,end_date)
    
    def del_mentorship(self,mentor_id,mentee_id):
        self.persons[mentee_id].mentor=None
        
        childs_origin=self.persons[mentor_id].childs
        childs_new=[]
        for child in childs_origin:
            if child[0].person_id!=mentee_id:
                childs_new.append(child)
        self.persons[mentor_id].childs=childs_new
        
        self.db.del_mentorship(mentor_id,mentee_id)
        
    def del_person(self):
        pass

    # 或许没用
    def to_db(self):
        db=self.db
        for person_id,person_node in self.persons.items():
            person_exists = db.exec(f"""
                                    SELECT COUNT(*) FROM person WHERE person_id = {person_id}
                                    """)
            if person_exists[0][0] == 0:
                db.exec(f"""
                    INSERT INTO person (person_id, name, profile_link)
                    VALUES ({person_id}, '{person_node.name}', '{person_node.profile_link}')
                    """)
            else:
                db.exec(f"""
                    UPDATE person
                    SET name = '{person_node.name}', profile_link = '{person_node.profile_link}'
                    WHERE person_id = {person_id}
                    """)
        for father_id,father in self.persons.items():
            for child in father.childs:
                rel_exists=db.exec(
                    f"""
                    SELECT COUNT(*) FROM mentorship WHERE mentor_id = {father_id} AND mentee_id={child[0].person_id}
                    """)
                if rel_exists[0][0] == 0:
                    mentorship_id=(father_id+child[0].person_id)%int(max_id)
                    db.exec(f"""
                            INSERT INTO mentorship (mentorship_id,smentor_id, mentee_id, start_date, end_date)
                            VALUES ({mentorship_id},{father_id}, {child[0].person_id}, '{child[1]}', '{child[2]}')
                            ON DUPLICATE KEY UPDATE start_date = %s, end_date = %s
                            """)
                else:
                    db.exec(f"""
                        UPDATE mentorship 
                        SET start_date='{child[1]}',end_date='{child[2]}'
                        WHERE mentor_id = {father_id} AND mentee_id={child[0].person_id}
                        """)     
    
    def check(self,name):
        ret={}
        for person_id,person_node in self.persons.items():
            if person_node.name==name:
                ret["me"]=name
                ret["mentee"]=person_node.childs
                ret["mentor"]=person_node.mentor
        return ret
   

    
        
