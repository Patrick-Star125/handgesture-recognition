import sys
from PyQt5.QtWidgets import QApplication
from Connect.use import Window


class connect:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.w = Window()
        self.w.show()

    # 接收运行Log，并进行操作
    def set_Log(self, log,img):
        self.w.reImg(img)
        self.w.set_Log(log,img)

    def getNum(self):
        return self.w.get_duoren()

    # 拿视频流
    def get_cap(self):
        return self.w.get_cap()

    # 拿选择的人的编号，字符串
    def get_choose_person_number(self):
        return self.w.get_choose_person_number()


if __name__ == '__main__':
    c = connect()
    sys.exit(c.app.exec_())

