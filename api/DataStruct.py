from database import Database
from typing import List
import hashlib
import time
from typing import Dict, Tuple
import numpy as np
import random
import json

max_id = 1000


class Node:
    def __init__(self, user_id=None):
        self.user_id: int = user_id
        # Node+mentorship_id
        self.mentees: List[List[Node, int]] = []
        self.mentors: List[List[Node, int]] = []


class AcdemicTree():
    def __init__(self, db: Database):
        self.db = db

        db_users = db.exec("""
                select * from user
                """)
        db_mentorships = db.exec(
            """
            select * from mentorship
            """
        )

        self.users: Dict[int, Node] = {}
        for user in db_users:
            user_node = Node(user[0])
            self.users[user[0]] = user_node

        for r in db_mentorships:
            mentorship_id = r[0]
            mentor_id = r[1]
            mentee_id = r[2]
            self.users[mentee_id].mentors.append([self.users[mentor_id], mentorship_id])
            self.users[mentor_id].mentees.append([self.users[mentee_id], mentorship_id])

    def get_random_institute(self):
        institutes = ["Institute A", "Institute B", "Institute C", "Institute D", "Institute E"]
        return random.choice(institutes)

    # 0 用户名已存在
    # 1 注册成功
    def register(self, user_name, password, identity):
        user_id = int(hashlib.sha256((user_name + password + identity).encode()).hexdigest(), 16) % int(max_id)
        if self.users.get(user_id):
            return 0
        newguy = Node(user_id=user_id)
        self.users[user_id] = newguy
        institute = self.get_random_institute()  # 随机生成institute值
        self.db.register(user_id=user_id, user_name=user_name, password=password, identity=identity,
                         institute=institute)
        return 1

    def check_user_exists(self, name: str) -> int:
        query = f"SELECT COUNT(*) FROM user WHERE user_name = '{name}'"
        result = self.db.exec(query)
        if result[0][0] > 0:
            return False
        else:
            return True

    def add_mentorship(self, mentor_id, mentee_id, start_date=None, end_date=None):
        if start_date == None:
            start_date = time.strftime("%Y-%m-%d", time.gmtime())
        if end_date == None:
            end_date = "1970-01-01"
        mentorship_id = (mentee_id + mentee_id) % int(max_id)
        self.users[mentee_id].mentors.append([self.users[mentor_id], mentorship_id])
        self.users[mentor_id].mentees.append([self.users[mentee_id], mentorship_id])
        self.db.add_mentorship(mentorship_id, mentor_id, mentee_id, start_date, end_date)

    def del_mentorship(self, mentor_id, mentee_id):
        mentors_origin = self.users[mentee_id].mentors
        mentors_new = []
        for mentor in mentors_origin:
            if mentor[0].user_id != mentor_id:
                mentors_new.append(mentor)
        self.users[mentee_id].mentors = mentors_new

        mentees_origin = self.users[mentor_id].mentees
        mentees_new = []
        for mentee in mentees_origin:
            if mentee[0].user_id != mentee_id:
                mentees_new.append(mentee)
        self.users[mentor_id].mentees = mentees_new
        self.db.del_mentorship(mentor_id, mentee_id)

    def del_person(self):
        pass

    # TODO:to be modified
    def check_relationship(self, real_name):
        def id2msg2json(user_id):
            db_ret = self.db.exec(f"""
                     select from user 
                     where real_name='{real_name}'
                     """)
            real_name = db_ret[0][4]
            profile_link = db_ret[0][5]
            js = {
                "name": real_name,
                "attributes": {
                    "link": profile_link
                },
            }
            return js

        db_ret = self.db.exec(f"""
                     select from user 
                     where real_name='{real_name}'
                     """)
        me_id = db_ret[0][0]
        me_js = id2msg2json(me_id)
        me_js["children"] = [id2msg2json(mentee[0].user_id for mentee in self.users[me_id].mentees)]
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
                "applicantTime": app[2].strftime("%Y-%m-%d %H:%M:%S"),  # 将 datetime 转换为字符串
                "item_id": app[1]
            }
            results.append(result)
        return results

    # 处理申请信息
    def process_application(self, item_id: int, result: str) -> Tuple[int, str]:
        application = self.db.exec(f"""
            SELECT applicant_name, respondent_name FROM application 
            WHERE item_id = {item_id}
        """)
        if not application:
            return 0, f"Error: application with item_id {item_id} does not exist."

        applicant_name, respondent_name = application[0]

        # 更新 application 表中的 is_processed 和 process_result
        self.db.exec(f"""
            UPDATE application 
            SET is_processed = TRUE, process_result = '{result}'
            WHERE item_id = {item_id}
        """)

        if result == "Yes":
            # 根据 applicant_name 和 respondent_name 获取对应的 user_id
            applicant_id = self.db.exec(f"SELECT user_id FROM user WHERE user_name = '{applicant_name}'")[0][0]
            respondent_id = self.db.exec(f"SELECT user_id FROM user WHERE user_name = '{respondent_name}'")[0][0]

            # 调用 add_mentorship 方法
            self.add_mentorship(mentor_id=respondent_id, mentee_id=applicant_id)

        return 1, f"Application with item_id {item_id} processed successfully with result {result}."

    # 管理员查询所有未处理的申请
    def get_Allapplications(self) -> List[Dict[str, str]]:
        unprocessed_apps = self.db.exec(f"""
            SELECT applicant_name, respondent_name, item_id, creation_time FROM application 
            WHERE is_processed = FALSE
        """)
        results = []
        for app in unprocessed_apps:
            result = {
                "applicantName": app[0],
                "respondentName": app[1],
                "item_id": app[2],
                "applicantTime": app[3].strftime("%Y-%m-%d %H:%M:%S")
            }
            results.append(result)
        return results

    def search_user(self, name: str, searchType: str) -> List[Dict[str, str]]:
        if searchType == "Name":
            query = f"SELECT real_name, institute, user_id FROM user WHERE real_name = '{name}'"
        elif searchType == "Institution":
            query = f"SELECT real_name, institute, user_id FROM user WHERE institute = '{name}'"
        else:
            return []  # 无效的 searchType，返回空列表

        results = self.db.exec(query)
        users = []
        for result in results:
            user = {
                "real_name": result[0],
                "institute": result[1],
                "user_id": result[2]
            }
            users.append(user)
        return users

    def locate_nodes(self, me_node: Node):
        nodes = []
        links = []

        def recursion(ments, x, y, flag, depth, fa_name):
            N = len(ments)
            if N % 2 == 1:
                x_lst = x + np.array(range(-int((N - 1) / 2), int((N + 1) / 2) + 1)) * 100
            else:
                x_lst = x + np.array(range(-(int(N / 2)), int(N / 2))) * 100 + 50

            if flag == 1:
                y_now = y - 100
            else:
                y_now = y + 100

            for x_now, node_now in zip(x_lst, ments):
                node_now = node_now[0]
                tmp_node_dic = {}
                s = self.db.get_user_info(node_now.user_id)
                tmp_node_dic["real_name"] = s[4]
                tmp_node_dic["user_id"] = node_now.user_id
                tmp_node_dic["x"] = int(x_now)
                tmp_node_dic["y"] = int(y_now)
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
                        recursion(node_now.mentors, x_now, y_now, flag, depth - 1, tmp_node_dic["real_name"])
                    else:
                        recursion(node_now.mentees, x_now, y_now, flag, depth - 1, tmp_node_dic["real_name"])

        me_x = 500
        me_y = 300
        me_dic = {}
        s = self.db.get_user_info(me_node.user_id)
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

