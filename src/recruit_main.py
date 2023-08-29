import json
import os
import pickle
import re

import sass
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QColor, QFont, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QFileDialog, QHeaderView,
                             QTableWidgetItem, QWidget)

from api.mainAPI import Approval, Recruit, Resume
from components.messagelabel import MessageLabel
from ui.main import Ui_Main


class RecruitMain(QWidget, Ui_Main):

    recruit = Recruit()

    def __init__(self, uid) -> None:
        self.uid = uid
        super(RecruitMain, self).__init__()
        self.setupUi(self)

        self.loadQss()
        self.initUI()

    def initUI(self):
        self.msgLabel = MessageLabel(self)
        self.msgLabel.setGeometry(0, 50, 380, 50)

        self.catalogUI()
        self.tableUI()
        
        self.loadRecruits()
        

        # 选中"招聘公告"这个item
        self.leftCatalog.setCurrentItem(self.leftCatalog.item(1))
        # 绑定某个item被点击的信号
        self.leftCatalog.currentItemChanged.connect(self.linkStackPages)
        # 设置面包屑根元素默认高亮
        self.recruitHeadTip.setProperty('state', 'highlight')
        self.recruitHeadTip.style().polish(self.recruitHeadTip)
        # 绑定表格点击事件
        self.recruitAllTableWidget.cellClicked.connect(self.selectReruit)
        # 绑定面包屑根元素点击事件
        self.recruitHeadTipClickable.clicked.connect(self.returnRecruit)

        self.submitBtn.clicked.connect(self.uploadResume)

        # 绑定公告ComboBox切换事件
        self.recruitComboBox.currentIndexChanged.connect(self.getPosition)
        self.appRecruitComboBox.currentIndexChanged.connect(self.showApproval)
        self.repRecruitComboBox.currentIndexChanged.connect(self.showReport)
        # 绑定文件选择按钮
        self.uploadBtn.clicked.connect(self.selectFile)

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

        # print(globalQss)

    def linkStackPages(self, index):
        if self.leftCatalog.currentItem().text() == "招聘公告":
            self.showRecruit(0)
            self.stackedWidget.setCurrentIndex(0)
        elif self.leftCatalog.currentItem().text() == "审批流程":
            self.showApproval()
            self.stackedWidget.setCurrentIndex(2)
        elif self.leftCatalog.currentItem().text() == "录用结果":
            self.showReport()
            self.stackedWidget.setCurrentIndex(3)
        elif self.leftCatalog.currentItem().text() == "简历投递":
            self.stackedWidget.setCurrentIndex(4)

    def catalogUI(self):
        firstItemFont = QFont()
        firstItemFont.setFamily("Microsoft YaHei UI")
        firstItemFont.setPointSize(14)
        firstItemFont.setBold(True)
        self.leftCatalog.addItem("信息公示 Information", level="1", first_style=firstItemFont)
        self.leftCatalog.addItem("招聘公告", level="2")
        self.leftCatalog.addItem("审批流程", level="2")
        self.leftCatalog.addItem("录用结果", level="2")
        self.leftCatalog.addItem("在线招聘  Recruit", level="1", first_style=firstItemFont)
        self.leftCatalog.addItem("简历投递", level="2")

    def tableUI(self):
        self.recruitAllTableWidget.setColumnCount(2)

        # 表格不显示网格线、列头、行头不显示
        self.recruitAllTableWidget.setShowGrid(False)
        self.recruitAllTableWidget.verticalHeader().setVisible(False)
        self.recruitAllTableWidget.horizontalHeader().setVisible(False)
        # 表格不可编辑
        self.recruitAllTableWidget.setEditTriggers(self.recruitAllTableWidget.NoEditTriggers)
        # 表格不显示选中
        self.recruitAllTableWidget.setFocusPolicy(False)
        # 设置列宽
        self.recruitAllTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.recruitAllTableWidget.setColumnWidth(1, 125)
        # 选中整行
        self.recruitAllTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 鼠标悬停时应用样式
        self.recruitAllTableWidget.viewport().setMouseTracking(True)
        self.recruitAllTableWidget.viewport().installEventFilter(self)
        self.row = 0  # hover行的默认值

    def eventFilter(self, obj, event):
        '''鼠标悬停事件行为过滤器'''
        # 如果这个事件发生在表格视口内
        if obj == self.recruitAllTableWidget.viewport():
            # 如果是鼠标移动事件
            if event.type() == QEvent.MouseMove:
                # 根据鼠标位置获取当前所在行
                index = self.recruitAllTableWidget.indexAt(event.pos())
                # 如果当前行有效
                if index.isValid():
                    # 如果当前行和上一次的行不一样
                    if self.row != index.row():
                        # 则将上一次的行背景色还原
                        for col in range(self.recruitAllTableWidget.columnCount()):
                            self.recruitAllTableWidget.item(self.row, col).setBackground(QColor("white"))
                        self.row = index.row()  # 更新当前行
                        # 设置当前行背景色
                        for col in range(self.recruitAllTableWidget.columnCount()):
                            self.recruitAllTableWidget.item(self.row, col).setBackground(QColor("#ECF5FF"))

        return super().eventFilter(obj, event)

    def showRecruit(self, recruit_id):
        '''显示招聘公告'''
        # num = int(1E6)
        # self.recruitAllTableWidget.setRowCount(num)
        # for i in range(num):
        #     title = QTableWidgetItem('title' + str(i))
        #     date = QTableWidgetItem('date' + str(i))
        #     self.recruitAllTableWidget.setItem(i, 0, title)
        #     self.recruitAllTableWidget.setItem(i, 1, date)
        # print('showRecruit')
        recruits = self.recruit.getRecruitInfo()
        self.recruitAllTableWidget.setRowCount(len(recruits))
        # print(recruits)
        for i in range(len(recruits)):
            # 填充至recruitAllTableWidget
            title = QTableWidgetItem(recruits[i]['title'])
            date = QTableWidgetItem(recruits[i]['releasetime'])
            self.recruitAllTableWidget.setItem(i, 0, title)
            self.recruitAllTableWidget.setItem(i, 1, date)

    def selectReruit(self, row, col):
        '''选中招聘公告'''
        rec = self.recruit.getRecruitInfo(row + 1)
        self.recruitTitleTip.setText(rec['title'])
        self.textEdit.setText(rec['content'])
        self.textEdit.setReadOnly(True)

        self.stackedWidget.setCurrentIndex(1)

    def returnRecruit(self):
        '''返回招聘公告页面'''
        self.stackedWidget.setCurrentIndex(0)

    def loadRecruits(self):
        '''简历投递页面'''

        self.IS_RESUME = 0
        self.recruitComboBox.clear()
        res = self.recruit.getRecruitInfo()
        recruitTitles = [str(i["rid"]) + "-" + i["title"] for i in res]
        self.recruitComboBox.addItems(recruitTitles)
        self.appRecruitComboBox.addItems(recruitTitles)
        self.repRecruitComboBox.addItems(recruitTitles)

    def getPosition(self):
        '''根据招聘公告，获取招聘信息的职位'''
        curRecruit = self.recruitComboBox.currentText()
        rid, title = curRecruit.split("-")
        res = self.recruit.getRecruitInfo(rid)
        positions = json.loads(res["position"])
        self.positionComboBox.clear()
        self.positionComboBox.addItems(positions)

        self.getOnlineResume()

    def getOnlineResume(self):
        '''获取在线简历'''
        self.resume = Resume()
        curResume = self.recruitComboBox.currentText()
        rid, title = curResume.split("-")
        res = self.resume.getResume(self.uid,int(rid))
        if res:
            self.nameLineEdit.setText(res["name"])
            self.ageLineEdit.setText(str(res["age"]))
            self.idLineEdit.setText(res["id_card"])
            self.educationalComboBox.setCurrentText(res["education"])
            self.positionComboBox.setCurrentText(res["job_position"])
            self.filepath = res["resume"]
            pixmap = QPixmap(self.filepath)
            pixmap = pixmap.scaled(self.photoPic.maximumSize(), 1)
            self.photoPic.setPixmap(pixmap)
            self.IS_RESUME = 1
            self.msgLabel.setMessage("已载入该招聘公告的简历")
            self.msgLabel.setMode("success")
            self.msgLabel.startAnimation()
        else:
            pass

    def selectFile(self):
        self.filepath = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                                    "Picture Files (*.jpg *.png)")
        if self.filepath[0] != "":
            self.filepath = self.filepath[0]
            self.IS_RESUME = 1
            pixmap = QPixmap(self.filepath)
            # 缩放图片，以适应label大小
            pixmap = pixmap.scaled(self.photoPic.maximumSize(), 1)
            self.photoPic.setPixmap(pixmap)

    def uploadResume(self):
        '''上传简历'''
        # 检查是否完善信息
        recContent = self.recruitComboBox.currentText()

        if recContent != "":
            rid, title = recContent.split("-")
        else:
            self.msgLabel.setMessage("请先选择招聘公告")
            self.msgLabel.setMode("error")
            self.msgLabel.startAnimation()
            return

        if self.maleRadioButton.isChecked():
            gender = "男"
        elif self.femaleRadioButton.isChecked():
            gender = "女"
        else:
            self.msgLabel.setMessage("请选择您的性别")
            self.msgLabel.setMode("error")
            self.msgLabel.startAnimation()
            return

        name = self.nameLineEdit.text()
        age = self.ageLineEdit.text()
        idNum = self.idLineEdit.text()
        education = self.educationalComboBox.currentText()
        position = self.positionComboBox.currentText()

        if name != "" and gender != "" and age != "" and idNum != "" and education != "" and position != "" and self.IS_RESUME:
            res = {
                "name": name,
                "gender": gender,
                "age": age,
                "idnum": idNum,
                "education": education,
                "position": position,
                "resumeFile": self.filepath,
                "rid": rid,
                "uid": self.uid,
            }
            # print(res)

            self.resume = Resume()
            self.resume.createResume(res)
            msg = self.resume.submitResume()
            self.msgLabel.setMessage(msg)
            self.msgLabel.setMode("success")
            self.msgLabel.startAnimation()
            return 1
        else:
            self.msgLabel.setMessage("请完善信息")
            self.msgLabel.setMode("error")
            self.msgLabel.startAnimation()
            return
        


    def showApproval(self):
        '''显示审批流程'''
        self.approval = Approval()
        curApp = self.appRecruitComboBox.currentText()
        rid, title = curApp.split("-")
        res = self.approval.getApproval(self.uid,int(rid))
        if res:
            if res["resume_delivery"] == 1:
                self.stepPic_1.setPixmap(QPixmap(":/header/img/pass.png"))
                self.stepTip_1.setProperty('state', 'pass')
                self.stepTip_1.style().polish(self.stepTip_1)
                self.stepMsg_1.setText("您已成功投递简历，您的应聘资质我们正在加快审查中，请留意您的邮箱，我们会第一时间给您回复！")
                self.stepTime_1.setText(res["resume_delivery_time"])
            elif res["resume_delivery"] == 0:
                self.stepMsg_1.setText("在当前招聘公告中，您尚未投递简历，您可以点击下方按钮投递简历，或切换招聘公告再次查询。")
                self.stepTip_1.setProperty('state', 'wait')
                self.stepTip_1.style().polish(self.stepTip_1)
                self.stepTime_1.setText("--.--.-- --:--:--")
            else:
                pass

            if res["online_exam"] == 1:
                self.stepPic_2.setPixmap(QPixmap(":/header/img/pass.png"))
                self.stepTip_2.setProperty('state', 'pass')
                self.stepTip_2.style().polish(self.stepTip_2)
                self.stepMsg_2.setText("您的应聘资质我们已经线上审查通过，接下来将交由工作人员进行线下审查，请留意您的邮箱或手机，我们会第一时间联系您！")
                self.stepTime_2.setText(res["online_exam_time"])
            elif res["online_exam"] == 0:
                self.stepMsg_2.setText("您的应聘资质我们正在线上审查中，请留意您的邮箱或手机，我们会第一时间联系您！")
                self.stepTip_2.setProperty('state', 'wait')
                self.stepTip_2.style().polish(self.stepTip_2)
                self.stepTime_2.setText("--.--.-- --:--:--")
            else:
                self.stepMsg_2.setText("您的应聘资质未通过线上审查，请留意您的邮箱或手机，我们会第一时间联系您！")
                self.stepTip_2.setProperty('state', 'fail')
                self.stepTip_2.style().polish(self.stepTip_2)
                self.stepTime_2.setText(res["online_exam_time"])
                self.stepPic_2.setPixmap(QPixmap(":/header/img/fail.png"))
            
            if res["offline_exam"] == 1:
                self.stepPic_3.setPixmap(QPixmap(":/header/img/pass.png"))
                self.stepTip_3.setProperty('state', 'pass')
                self.stepTip_3.style().polish(self.stepTip_3)
                self.stepMsg_3.setText("您的应聘资质我们已经审查通过，恭喜您进入笔试环节。具体事项和笔试地点请留意你的邮箱或手机短信。")
                self.stepTime_3.setText(res["offline_exam_time"])
            elif res["offline_exam"] == 0:
                self.stepMsg_3.setText("您的应聘资质我们正在审查中，请留意您的邮箱或手机，我们会第一时间联系您！")
                self.stepTip_3.setProperty('state', 'wait')
                self.stepTip_3.style().polish(self.stepTip_3)
                self.stepTime_3.setText("--.--.-- --:--:--")
            else:
                self.stepMsg_3.setText("对不起，您的应聘资质未通过线下审查，感谢您的参与！")
                self.stepTip_3.setProperty('state', 'fail')
                self.stepTip_3.style().polish(self.stepTip_3)
                self.stepTime_3.setText(res["offline_exam_time"])
                self.stepPic_3.setPixmap(QPixmap(":/header/img/fail.png"))

            if res["written_exam"] == 1:
                self.stepPic_4.setPixmap(QPixmap(":/header/img/pass.png"))
                self.stepTip_4.setProperty('state', 'pass')
                self.stepTip_4.style().polish(self.stepTip_4)
                self.stepMsg_4.setText("恭喜您通过笔试环节，接下来将进入面试环节。具体事项和面试地点请留意你的邮箱或手机短信。")
                self.stepTime_4.setText(res["written_exam_time"])
            elif res["written_exam"] == 0:
                self.stepMsg_4.setText("您的笔试试卷我们正在批阅中，请留意您的邮箱或手机，我们会第一时间联系您！")
                self.stepTip_4.setProperty('state', 'wait')
                self.stepTip_4.style().polish(self.stepTip_4)
                self.stepTime_4.setText("--.--.-- --:--:--")
            else:
                self.stepMsg_4.setText("对不起，您的笔试试卷未通过审阅，感谢您的参与！")
                self.stepTip_4.setProperty('state', 'fail')
                self.stepTip_4.style().polish(self.stepTip_4)
                self.stepTime_4.setText(res["written_exam_time"])
                self.stepPic_4.setPixmap(QPixmap(":/header/img/fail.png"))
            
            if res["interview"] == 1:
                self.stepPic_5.setPixmap(QPixmap(":/header/img/pass.png"))
                self.stepTip_5.setProperty('state', 'pass')
                self.stepTip_5.style().polish(self.stepTip_5)
                self.stepMsg_5.setText("恭喜您已通过面试环节，面试得分为xx.xx。您已被本司拟录用，请回复邮件或短信确认，期待您的加入！")
                self.stepTime_5.setText(res["interview_time"])
            elif res["interview"] == 0:
                self.stepMsg_5.setText("您的面试我们正在安排中，请留意您的邮箱或手机，我们会第一时间联系您！")
                self.stepTip_5.setProperty('state', 'wait')
                self.stepTip_5.style().polish(self.stepTip_5)
                self.stepTime_5.setText("--.--.-- --:--:--")
            else:
                self.stepMsg_5.setText("对不起，您的面试未通过，感谢您的参与！")
                self.stepTime_5.setText(res["interview_time"])
                self.stepTip_5.setProperty('state', 'fail')
                self.stepTip_5.style().polish(self.stepTip_5)
                self.stepPic_5.setPixmap(QPixmap(":/header/img/fail.png"))
        else:
            self.stepMsg_1.setText("在当前招聘公告中，您尚未投递简历，您可以点击下方按钮投递简历，或切换招聘公告再次查询。")
            self.stepPic_1.setPixmap(QPixmap(":/header/img/wait.png"))
            self.stepTip_1.setProperty('state', 'wait')
            self.stepTip_1.style().polish(self.stepTip_1)
            self.stepTime_1.setText("--.--.-- --:--:--")

            self.stepMsg_2.setText("您在当前招聘公告中，您尚未投递简历，您可以点击下方按钮投递简历，或切换招聘公告再次查询。")
            self.stepPic_2.setPixmap(QPixmap(":/header/img/wait.png"))
            self.stepTip_2.setProperty('state', 'wait')
            self.stepTip_2.style().polish(self.stepTip_2)
            self.stepTime_2.setText("--.--.-- --:--:--")

            self.stepMsg_3.setText("在当前招聘公告中，您尚未投递简历，您可以点击下方按钮投递简历，或切换招聘公告再次查询。")
            self.stepPic_3.setPixmap(QPixmap(":/header/img/wait.png"))
            self.stepTip_3.setProperty('state', 'wait')
            self.stepTip_3.style().polish(self.stepTip_3)
            self.stepTime_3.setText("--.--.-- --:--:--")

            self.stepMsg_4.setText("在当前招聘公告中，您尚未投递简历，您可以点击下方按钮投递简历，或切换招聘公告再次查询。")
            self.stepPic_4.setPixmap(QPixmap(":/header/img/wait.png"))
            self.stepTip_4.setProperty('state', 'wait')
            self.stepTip_4.style().polish(self.stepTip_4)
            self.stepTime_4.setText("--.--.-- --:--:--")

            self.stepMsg_5.setText("在当前招聘公告中，您尚未投递简历，您可以点击下方按钮投递简历，或切换招聘公告再次查询。")
            self.stepPic_5.setPixmap(QPixmap(":/header/img/wait.png"))
            self.stepTip_5.setProperty('state', 'wait')
            self.stepTip_5.style().polish(self.stepTip_5)
            self.stepTime_5.setText("--.--.-- --:--:--")


    def showReport(self):
        self.resume = Resume()
        curApp = self.repRecruitComboBox.currentText()
        rid, title = curApp.split("-")
        res = self.resume.getResume(self.uid,int(rid))
        if res:
            self.nameLabel.setText(res["name"])
            self.ageLabel.setText(str(res["age"]))
            self.idLabel.setText(res["id_card"])
            self.genderLabel.setText("男" if res["gender"] == 1 else "女")
            pixmap = QPixmap(res["resume"])
            # 缩放图片，以适应label大小
            pixmap = pixmap.scaled(self.picLabel.maximumSize(), 1)
            self.picLabel.setPixmap(pixmap)
        else:
            self.msgLabel.setMessage("该公告下无简历信息！")
            self.msgLabel.setMode("error")
            self.msgLabel.startAnimation()
            return
 
        self.approval = Approval()
        curApp = self.repRecruitComboBox.currentText()
        rid, title = curApp.split("-")
        res = self.approval.getApproval(self.uid,int(rid))
        if res:
            if res["written_exam_score"] and res["written_exam_score"] >= 60:
                self.writtenExamLabel.setText(str(res["written_exam_score"]))
                self.writtenExamLabel.setProperty('state', 'pass')
                self.writtenExamLabel.style().polish(self.writtenExamLabel)
            elif res["written_exam_score"] and res["written_exam_score"] < 60:
                self.writtenExamLabel.setText(str(res["written_exam_score"]))
                self.writtenExamLabel.setProperty('state', 'fail')
                self.writtenExamLabel.style().polish(self.writtenExamLabel)
            else:
                self.writtenExamLabel.setText("--")
                self.writtenExamLabel.setProperty('state', 'wait')
                self.writtenExamLabel.style().polish(self.writtenExamLabel)
            
            if res["interview_score"] and res["interview_score"] >= 60:
                self.interviewLabel.setText(str(res["interview_score"]))
                self.interviewLabel.setProperty('state', 'pass')
                self.interviewLabel.style().polish(self.interviewLabel)
            elif res["interview_score"] and res["interview_score"] < 60:
                self.interviewLabel.setText(str(res["interview_score"]))
                self.interviewLabel.setProperty('state', 'fail')
                self.interviewLabel.style().polish(self.interviewLabel)
            else:
                self.interviewLabel.setText("--")
                self.interviewLabel.setProperty('state', 'wait')
                self.interviewLabel.style().polish(self.interviewLabel)
            if res['total_score'] and res['total_score'] >= 60:
                self.totalLabel.setText(str(res["total_score"]))
                self.totalLabel.setProperty('state', 'pass')
                self.totalLabel.style().polish(self.totalLabel)
            elif res['total_score'] and res['total_score'] < 60:
                self.totalLabel.setText(str(res["total_score"]))
                self.totalLabel.setProperty('state', 'fail')
                self.totalLabel.style().polish(self.totalLabel)
            else:
                self.totalLabel.setText("--")
                self.totalLabel.setProperty('state', 'wait')
                self.totalLabel.style().polish(self.totalLabel)
            if res['rank']:
                self.rankLabel.setText(res["rank"])
            else:
                self.rankLabel.setText("--")
            if res['is_hired']:
                self.isHiredLabel.setText("已录用")
                self.isHiredLabel.setProperty('state', 'pass')
                self.isHiredLabel.style().polish(self.isHiredLabel)
            else:
                self.isHiredLabel.setText("未录用")
                self.isHiredLabel.setProperty('state', 'fail')
                self.isHiredLabel.style().polish(self.isHiredLabel)
        else:
            return