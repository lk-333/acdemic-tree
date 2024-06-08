from database import Database
from DataStruct import *
if __name__=="__main__":
    db=Database()
    acdemic_tree=AcdemicTree(db)
    # db.add_person(name="ZhiyiHou",profile="cccc")
    # db.add_mentorship(mentor_id=111,mentee_id=333)
    # db.add_user(user_name="口口口口口",password=888888)
    acdemic_tree.add_person(name="KongZi",profile_link="www.kongzi.com")
    acdemic_tree.to_db()
    