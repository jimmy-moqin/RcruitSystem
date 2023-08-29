from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel


class CaptchaLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(CaptchaLabel, self).__init__(parent)
        self.code = ""
        self.q_image = None

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setPixMap(self, q_image):
        self.q_image = q_image
        self.setPixmap(q_image)
    
    def mousePressEvent(self, event):
        self.clicked.emit()
        return super(CaptchaLabel, self).mousePressEvent(event)