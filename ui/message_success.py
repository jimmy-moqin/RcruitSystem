# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\接单\1958756124713311871人力资源管理软件\XuanYuRecruit/ui/message_success.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MessageSuccess(object):
    def setupUi(self, MessageSuccess):
        MessageSuccess.setObjectName("MessageSuccess")
        MessageSuccess.resize(380, 50)
        self.label = QtWidgets.QLabel(MessageSuccess)
        self.label.setGeometry(QtCore.QRect(18, 15, 20, 20))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/message/img/success.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(MessageSuccess)
        self.label_2.setGeometry(QtCore.QRect(51, 16, 281, 16))
        font = QtGui.QFont()
        font.setFamily("思源黑体 CN")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(MessageSuccess)
        self.label_3.setGeometry(QtCore.QRect(350, 20, 10, 10))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/message/img/close.png"))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(MessageSuccess)
        QtCore.QMetaObject.connectSlotsByName(MessageSuccess)

    def retranslateUi(self, MessageSuccess):
        _translate = QtCore.QCoreApplication.translate
        MessageSuccess.setWindowTitle(_translate("MessageSuccess", "Form"))
        self.label_2.setText(_translate("MessageSuccess", "注册成功"))
from resource.qrc import loginQrc_rc
