import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget


# second ui
class sanUI(QWidget):
    def __init__(self):
        super(sanUI, self).__init__()
        self.resize(400, 100)
        self.setWindowTitle("确认")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(170, 0, 181, 91))
        self.label.setText("选择成功")
