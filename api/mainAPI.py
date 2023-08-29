import sqlite3
from datetime import datetime
from time import time


class Recruit(object):

    def __init__(self) -> None:
        self.conn = sqlite3.connect('./database/xuanyu.db')

    def getRecruitInfo(self, recruit_id=0):
        '''
        获取招聘信息
        '''
        if recruit_id == 0:
            # 全部招聘信息的标题title
            try:
                cursor = self.conn.cursor()
                cursor.execute('select rid, title, releasetime from recruitinfo')
                result = cursor.fetchall()
                cursor.close()
                res = []
                for i in result:
                    res.append({'rid': i[0], 'title': i[1], 'releasetime': i[2]})
                return res
            except Exception as e:
                print(e)
                return []
        else:
            # 指定rid的招聘信息
            try:
                cursor = self.conn.cursor()
                cursor.execute('select * from recruitinfo where rid = ?', (recruit_id, ))
                result = cursor.fetchone()
                cursor.close()
                res = {
                    'rid': result[0],
                    'title': result[1],
                    'releasetime': result[3],
                    'content': result[2],
                    'position': result[4]
                }
                return res
            except Exception as e:
                print(e)
                return []


class Resume(object):

    def __init__(self) -> None:
        self.conn = sqlite3.connect('./database/xuanyu.db')

        
    def createResume(self,resume):
        self.name = resume['name']
        self.gender = resume["gender"]
        self.age = resume['age']
        self.id_card = resume['idnum']
        self.education = resume['education']
        self.position = resume['position']
        self.resumeFile = resume['resumeFile']
        self.recruit_id = resume['rid']
        self.uid = resume['uid']

        self.approval_id = str(int(time()))

    def submitResume(self):
        try:
            cursor = self.conn.cursor()
            # 在插入之前先验证该用户是否已经投递过该招聘信息
            cursor.execute('select * from resumeinfo where recruit_id = ? and user_id = ?', (int(self.recruit_id), self.uid))
            result = cursor.fetchone()
            if result:
                return "您已经投递过该招聘信息"
            else:
                pass
            
            query = '''
                INSERT INTO resumeinfo (name, gender, age, id_card, education, job_position, resume, approval_id,user_id,recruit_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            data = (
                self.name, self.gender, self.age, self.id_card, self.education,
                self.position, self.resumeFile, self.approval_id, self.uid, self.recruit_id
            )
            cursor.execute(query, data)
            self.conn.commit()
            print("Record inserted successfully.")
            
            # 将投递信息插入到approvalinfo表中
            cursor.execute('INSERT INTO approvalinfo (uid, aid, rid, resume_delivery, resume_delivery_time) VALUES (?, ?, ?, ?, ?)', (self.uid, self.approval_id, self.recruit_id,1, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            self.conn.commit() # 提交事务

            return "投递成功"
        
        except sqlite3.Error as e:
            print("Error:", e)
            self.conn.rollback()
        finally:
            cursor.close()

    def getResume(self,uid,rid):
        try:
            cursor = self.conn.cursor()
            cursor.execute('select * from resumeinfo where user_id = ? and recruit_id = ?', (uid, rid))
            result = cursor.fetchone()
            if result:
                res ={
                    'name': result[1],
                    "gender": result[2],
                    'age': result[3],
                    'id_card': result[4],
                    'education': result[5],
                    'job_position': result[6],
                    'resume': result[7],
                    'approval_id': result[8],
                    'user_id': result[9],
                    'recruit_id': result[10],
                }
                return res
            else:
                return []
        except Exception as e:
            print(e)
            return []
        finally:
            cursor.close()

class Approval(object):
    def __init__(self):
        self.conn = sqlite3.connect('./database/xuanyu.db')
    
    

    def getApproval(self,uid,rid):
        try:
            cursor = self.conn.cursor()
            cursor.execute('select * from approvalinfo where uid = ? AND rid = ?', (uid, rid))
            result = cursor.fetchone()
            if result:
                res = {
                    'uid': result[0],
                    'aid': result[1],
                    'rid': result[2],
                    'resume_delivery': result[3],
                    'resume_delivery_time': result[4],
                    'online_exam': result[5],
                    'online_exam_time': result[6],
                    'offline_exam': result[7],
                    'offline_exam_time': result[8],
                    'written_exam': result[9],
                    'written_exam_time': result[10],
                    'written_exam_score': result[11],
                    'interview': result[12],
                    'interview_time': result[13],
                    'interview_score': result[14],
                    'total_score': result[15],
                    'rank': result[16],
                    'is_hired': result[17],
                }
                return res
            else:
                return []
        except Exception as e:
            print(e)
            return []
        finally:
            cursor.close()