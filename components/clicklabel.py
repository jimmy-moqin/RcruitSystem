from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel


class ClickLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(ClickLabel, self).__init__(*args, **kwargs)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        else:
            super(ClickLabel, self).mousePressEvent(event)