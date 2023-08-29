import os
import pickle
import re

import sass
from PyQt5.QtWidgets import QWidget

from api.loginAPI import Captcha, Login, Register
from src.recruit_main import RecruitMain
from ui.login import Ui_LoginWidget
from ui.login_log import Ui_log
from ui.login_reg import Ui_reg


class LoginMain(QWidget, Ui_LoginWidget):
    LOG_SHOW = 1
    REG_SHOW = 0

    PHONE_NUM_VALID = 0
    PWD_STRONG = 0
    EMAIL_VALID = 0
    CAPTCHA_TRUE = 0

    captcha = Captcha()

    def __init__(self):
        super(LoginMain, self).__init__()

        self.setupUi(self)
        Ui_log().setupUi(self.logWidget)

        Ui_reg().setupUi(self.regWidget)

        self.regWidget.hide()

        self.loadQss()
        self.loadCache()
        self.initUI()

    def initUI(self):

        self.logWidget.findChild(QWidget, 'transToRegisterBtn').clicked.connect(self.changePage)
        self.regWidget.findChild(QWidget, 'retLoginBtn').clicked.connect(self.changePage)
        self.regWidget.findChild(QWidget, 'captchaPicLabel').clicked.connect(self.changeCaptcha)
        self.regWidget.findChild(QWidget, 'phoneNumLineEdit').editingFinished.connect(self.checkPhoneNum)
        self.regWidget.findChild(QWidget, 'regPwdLineEdit').editingFinished.connect(self.checkPwdStrong)
        self.regWidget.findChild(QWidget, 'mailLineEdit').editingFinished.connect(self.checkMail)
        self.regWidget.findChild(QWidget, 'captchaLineEdit').editingFinished.connect(self.checkCaptcha)
        self.regWidget.findChild(QWidget, 'registerBtn').clicked.connect(self.register)
        self.logWidget.findChild(QWidget, 'accountLineEdit').editingFinished.connect(self.checkAccount)
        self.logWidget.findChild(QWidget, 'loginBtn').clicked.connect(self.login)

    def loadCache(self):
        if os.path.exists("./cache/logincache.pkl"):
            with open("./cache/logincache.pkl", "rb") as f:
                cache = pickle.load(f)
                self.logWidget.findChild(QWidget, 'accountLineEdit').setText(cache["account"])
                self.logWidget.findChild(QWidget, 'pwdLineEdit').setText(cache["pwd"])
                self.logWidget.findChild(QWidget, 'remindPwdCheckBox').setChecked(True)
        else:
            pass

    def loadQss(self):
        '''加载qss样式'''
        scss = ''
        for dirs, subdirs, files in os.walk('./resource/qss'):
            for file in files:
                if file.endswith('.scss') and file != 'common.scss':
                    with open(dirs + '/' + file, 'r', encoding='utf-8') as f:
                        scss = scss + f.read()
        globalQss = sass.compile(string=scss)
        self.setStyleSheet(globalQss)

    def changePage(self):
        '''点击注册账号或返回登录按钮时切换页面'''
        if self.LOG_SHOW:
            self.regWidget.show()
            self.logWidget.hide()
            self.LOG_SHOW = 0
            self.REG_SHOW = 1
            self.changeCaptcha()
        else:
            self.regWidget.hide()
            self.logWidget.show()
            self.LOG_SHOW = 1
            self.REG_SHOW = 0

    def changeCaptcha(self):
        '''点击验证码图片时刷新验证码'''
        code, q_image = self.captcha.get_captcha()
        self.regWidget.findChild(QWidget, 'captchaPicLabel').setPixmap(q_image)
        self.regWidget.findChild(QWidget, 'captchaPicLabel').setCode(code)

    def checkPhoneNum(self):
        '''检查手机号码是否合法'''
        pattern = r'^1[3456789]\d{9}$'
        phoneNum = self.regWidget.findChild(QWidget, 'phoneNumLineEdit').text()
        if re.match(pattern, phoneNum):
            if self.regWidget.findChild(QWidget, 'phoneNumTip').text() != '':
                self.regWidget.findChild(QWidget, 'phoneNumTip').setText('')
            else:
                pass
            self.PHONE_NUM_VALID = 1
        else:
            if phoneNum == '':
                self.regWidget.findChild(QWidget, 'phoneNumTip').setText('手机号码不能为空')
            else:
                self.regWidget.findChild(QWidget, 'phoneNumTip').setText('手机号码格式错误')
            self.PHONE_NUM_VALID = 0

    def checkPwdStrong(self):
        '''检查密码强度'''
        pwd = self.regWidget.findChild(QWidget, 'regPwdLineEdit').text()
        if 0 < len(pwd) < 6:
            self.regWidget.findChild(QWidget, 'regPwdTip').setText('密码长度不能少于8位')
            self.PWD_STRONG = 0
            return
        elif len(pwd) == 0:
            self.regWidget.findChild(QWidget, 'regPwdTip').setText('密码不能为空')
            self.PWD_STRONG = 0
            return

        # 至少包含两种字符类型的正则表达式模式
        patterns = [
            r'[A-Z]',  # 大写字母
            r'[a-z]',  # 小写字母
            r'[0-9]',  # 数字
            r'[!@#\$%\^&\*\(\),\.\?":\{\}\|<>]',  # 特殊字符
        ]

        # 检查是否满足至少两种字符类型的要求
        matches = sum(1 for pattern in patterns if re.search(pattern, pwd))

        if matches >= 2:
            if self.regWidget.findChild(QWidget, 'regPwdTip').text() != '':
                self.regWidget.findChild(QWidget, 'regPwdTip').setText('')
            else:
                pass
            self.PWD_STRONG = 1
        else:
            self.regWidget.findChild(QWidget, 'regPwdTip').setText('密码至少包含两种字符类型')
            self.PWD_STRONG = 0

    def checkMail(self):
        '''检查邮箱是否合法'''
        pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
        email = self.regWidget.findChild(QWidget, 'mailLineEdit').text()
        if re.match(pattern, email):
            if self.regWidget.findChild(QWidget, 'mailTip').text() != '':
                self.regWidget.findChild(QWidget, 'mailTip').setText('')
            else:
                pass
            self.EMAIL_VALID = 1
        else:
            if email == '':
                self.regWidget.findChild(QWidget, 'mailTip').setText('邮箱不能为空')
            else:
                self.regWidget.findChild(QWidget, 'mailTip').setText('邮箱格式错误')
            self.EMAIL_VALID = 0

    def checkCaptcha(self):
        '''检查验证码是否正确'''
        code = self.regWidget.findChild(QWidget, 'captchaLineEdit').text()
        if code == self.regWidget.findChild(QWidget, 'captchaPicLabel').getCode():
            if self.regWidget.findChild(QWidget, 'captchaTip').text() != '':
                self.regWidget.findChild(QWidget, 'captchaTip').setText('')
            else:
                pass
            self.CAPTCHA_TRUE = 1
        else:
            self.regWidget.findChild(QWidget, 'captchaTip').setText('验证码错误')
            self.changeCaptcha()
            self.CAPTCHA_TRUE = 0

    def checkAccount(self):
        '''检查账号是否输入合法'''
        patterns = [
            r'^1[3456789]\d{9}$',  # 手机号码
        ]
        account = self.logWidget.findChild(QWidget, 'accountLineEdit').text()
        if re.match(patterns[0], account):
            if self.logWidget.findChild(QWidget, 'accountTip').text() != '':
                self.logWidget.findChild(QWidget, 'accountTip').setText('')
            else:
                pass
            return True
        else:
            if account == '':
                self.logWidget.findChild(QWidget, 'accountTip').setText('账号不能为空')
            else:
                self.logWidget.findChild(QWidget, 'accountTip').setText('账号应为手机号')
            return False

    def login(self):

        log = Login(
            self.logWidget.findChild(QWidget, 'accountLineEdit').text(),
            self.logWidget.findChild(QWidget, 'pwdLineEdit').text())
        ret = log.login()
        code = ret['code']
        msg = ret['msg']
        if code == 200:
            self.msgWidget.setMode("success")
            self.msgWidget.setMessage(msg)
            self.uid = ret['uid']
            self.msgWidget.startAnimation()
            if self.logWidget.findChild(QWidget, 'remindPwdCheckBox').isChecked():
                cache = {
                    "account": self.logWidget.findChild(QWidget, 'accountLineEdit').text(),
                    "pwd": self.logWidget.findChild(QWidget, 'pwdLineEdit').text()
                }
                with open('./cache/logincache.pkl', 'wb') as f:
                    pickle.dump(cache, f)
            else:
                pass

            self.close()
            self.recruitMain = RecruitMain(self.uid)
            self.recruitMain.show()

        else:
            self.msgWidget.setMode("error")
            self.msgWidget.setMessage(msg)
            self.msgWidget.startAnimation()

    def reg_checkAll(self):
        '''检查所有输入是否合法'''
        self.checkPhoneNum()
        self.checkPwdStrong()
        self.checkMail()
        self.checkCaptcha()

        if self.PHONE_NUM_VALID and self.PWD_STRONG and self.EMAIL_VALID and self.CAPTCHA_TRUE:
            phoneNum = self.regWidget.findChild(QWidget, 'phoneNumLineEdit').text()
            mail = self.regWidget.findChild(QWidget, 'mailLineEdit').text()
            pwd = self.regWidget.findChild(QWidget, 'regPwdLineEdit').text()

            self.registerInfo = Register(phoneNum, mail, pwd)
            return True
        else:
            return False

    def register(self):
        '''注册'''
        if self.reg_checkAll():
            ret = self.registerInfo.submit()
            code = ret['code']
            msg = ret['msg']
            if code == 200:
                self.msgWidget.setMode("success")
                self.msgWidget.setMessage(msg)
                self.msgWidget.startAnimation()
                # self.changePage()
            else:
                self.msgWidget.setMode("error")
                self.msgWidget.setMessage(msg)
                self.msgWidget.startAnimation()
        else:
            self.msgWidget.setMode("error")
            self.msgWidget.setMessage("请检查输入是否合法")
            self.msgWidget.startAnimation()
