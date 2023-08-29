from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QRect, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QProxyStyle,
                             QSizePolicy, QSpacerItem, QStyle, QVBoxLayout,
                             QWidget)


class MessageLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 上移到顶层
        self.raise_()


    def setupUi(self,parent):
        self.messageContainer = QWidget(parent)
        self.messageContainer.setObjectName("messageContainer")
        self.messageContainer.setGeometry(QRect(0, -50, 380, 50))

        self.label = QLabel(self.messageContainer)
        self.label.setGeometry(QRect(18, 15, 20, 20))  
        self.label.setPixmap(QPixmap(":/message/img/success.png"))
        self.label.setObjectName("label")

        self.label_2 = QLabel(self.messageContainer)
        self.label_2.setGeometry(QRect(51, 16, 281, 16))  
        font = QFont()
        font.setFamily("思源黑体 CN")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("msgLabel")
        self.label_2.setText("注册成功")
        self.label_2.setProperty("type","success")


        self.label_3 = QLabel(self.messageContainer)
        self.label_3.setGeometry(QRect(350, 20, 10, 10))  # 初始位置在上方
        self.label_3.setPixmap(QPixmap(":/message/img/close.png"))
        self.label_3.setObjectName("label_3")
    
    def startAnimation(self):
        # 设置动画
        self.animation = QPropertyAnimation(self.messageContainer, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setStartValue(QRect(0, -50, 380, 50))
        self.animation.setEndValue(QRect(0, 0, 380, 50))
        self.animation.start()

        # 设置定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.hideAnimation)
        self.timer.start(1500)

    def hideAnimation(self):
        # 设置动画
        self.animation = QPropertyAnimation(self.messageContainer, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setStartValue(QRect(0, 0, 380, 50))
        self.animation.setEndValue(QRect(0, -50, 380, 50))
        self.animation.start()
        # 动画执行一次后停止
        self.timer.stop()

    def setMessage(self, msg):
        self.label_2.setText(msg)
    
    def setMode(self,mode):
        if mode == "success":
            self.messageContainer.setProperty("type","success")
            self.label_2.setProperty("type","success")
            self.label.setPixmap(QPixmap(":/message/img/success.png"))
        elif mode == "error":
            self.messageContainer.setProperty("type","error")
            self.label_2.setProperty("type","error")
            self.label.setPixmap(QPixmap(":/message/img/error.png"))
        else:
            raise Exception("mode error")
        self.messageContainer.style().polish(self.messageContainer)
        self.label_2.style().polish(self.label_2)


    


        

    