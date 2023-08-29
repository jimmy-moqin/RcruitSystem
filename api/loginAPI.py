import hashlib
import random
import sqlite3

import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap


class Captcha:

    def __init__(self, code_length=4, image_width=114, image_height=39):
        self.code_length = code_length
        self.image_width = image_width
        self.image_height = image_height

    def generate_random_code(self):
        code = ""
        for _ in range(self.code_length):
            code += str(random.randint(0, 9))
        return code

    def create_verification_code_image(self, code):
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)

        # Use np.uint8 as the depth for the image
        image = np.ones((self.image_height, self.image_width, 3), dtype=np.uint8) * background_color

        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(code, font, 1, 2)[0]
        x = int((self.image_width - text_size[0]) / 2)
        y = int((self.image_height + text_size[1]) / 2)
        cv2.putText(image, code, (x, y), font, 1, text_color, 2, cv2.LINE_AA)

        return image

    def get_captcha(self):
        code = self.generate_random_code()
        image = self.create_verification_code_image(code)
        cv2.imwrite("captcha.jpg", image)

        # Convert OpenCV image to QPixmap
        q_image = QImage("captcha.jpg")
        q_image = QPixmap.fromImage(q_image)

        return code, q_image


class Register(object):

    def __init__(self, phoneNum, mail, pwd):
        self.phoneNum = phoneNum
        self.mail = mail
        self.pwd = pwd

    def submit(self):
        '''提交注册信息'''
        print(self.phoneNum, self.mail, self.pwd)
        pwd = hashlib.md5(self.pwd.encode('utf-8')).hexdigest()

        # 连接sqlite3数据库
        try:
            conn = sqlite3.connect('./database/xuanyu.db')
            cursor = conn.cursor()
            # 先查询手机号码是否已经注册
            cursor.execute("SELECT phonenum FROM userinfo WHERE phonenum=?", (self.phoneNum,))
            result = cursor.fetchone()
            if result:
                ret = {"code":101, "msg":"手机号码已经注册"}
                return ret
            
            # 插入数据
            cursor.execute("INSERT INTO userinfo (phonenum, email, password, isonline, isadmin) VALUES (?, ?, ?, ?, ?)",
                        (self.phoneNum, self.mail, pwd, 0, 0))
            # 提交事务
            conn.commit()
            ret = {"code":200, "msg":"恭喜您注册成功, 请返回登录！"}
            # 关闭数据库连接
            conn.close()
            return ret
        except Exception as e:
            print(e)
            ret = {"code":102, "msg":e}
            return ret
        finally:
            conn.close()

class Login(object):
    def __init__(self,account,pwd) -> None:
        self.account = account
        self.pwd = pwd

    def login(self):
        pwdmd5 = hashlib.md5(self.pwd.encode('utf-8')).hexdigest()
        try:
            conn = sqlite3.connect('./database/xuanyu.db')
            cursor = conn.cursor()
            cursor.execute("SELECT phonenum, password, uid FROM userinfo WHERE phonenum=?", (self.account,))
            result = cursor.fetchone()
            if result:
                if result[1] == pwdmd5:
                    ret = {"code":200, "msg":"登录成功","uid":result[2]}
                    return ret
                else:
                    ret = {"code":101, "msg":"密码错误"}
                    return ret
            else:
                ret = {"code":102, "msg":"账号不存在"}
                return ret
        except Exception as e:
            print(e)
            ret = {"code":103, "msg":e}
            return ret
        finally:
            conn.close()