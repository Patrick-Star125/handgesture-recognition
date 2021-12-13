import cv2
import win32gui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, QtCore, QtWidgets
from Connect.gui import Ui_mainWindow
from Connect.control_win import *
from Connect.control_office import *
from Connect.states_html import *
import numpy as np
import json
from MQTT.mqttconnect import *

from Connect.new_show import SecondUI


def close_system():
    app = QApplication.instance()
    # 退出应用程序
    app.quit()


class Window(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        # 定义一些常规变量
        self.second_ui = SecondUI()
        self.status = 0
        self.xy_number = []
        self.log = ""
        self.json_str = ""
        self.now_type = ""
        self.hands_number = ""
        self.person_number = "0"
        self.show_states = 0  # 表示两个状态的切换
        self.is_starts = 0  # 表示摄像头是否启动
        self.mqtt = mqttConnect()
        self.biaoji = 0
        self.error = ""
        self.str = None

        # 实例化控制类
        self.c_win = control_win()
        self.c_off = control_office()
        self.c_states = states_html()

        # 关于界面
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture(0)  # 视频流
        ret, self.show_img = self.cap.read()
        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        self.slot_init()  # 初始化槽函数

    # 返回视频流
    def get_cap(self):
        return self.cap

    def get_choose_person_number(self):
        return self.second_ui.get_choose_person()

    # 接收Log
    def set_action_Log(self, log):
        self.textBrowser.append("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
                                "margin-right:0px; -qt-block-indent:0; ""text-indent:0px;\">" + log + "</p></body></html>")

    # 槽函数
    def slot_init(self):
        # 若该按键被点击，则调用button_open_camera_clicked()
        self.pushButton.clicked.connect(self.button_open_camera_clicked)
        # 若定时器结束，则调用show_camera()
        self.timer_camera.timeout.connect(self.show_camera)
        self.pushButton_2.clicked.connect(self.choose_main)
        self.pushButton_3.clicked.connect(self.change_biaoji)
        self.pushButton_4.clicked.connect(self.change_new_states_one)
        self.pushButton_5.clicked.connect(self.change_new_states_two)

    # 选择控制人
    def choose_main(self):
        self.second_ui.show()
        self.second_ui.is_open = 1
        self.str = self.lineEdit.text()

    def change_biaoji(self):
        self.biaoji = 1

    def get_duoren(self):
        return self.str

    def get_biaoji(self):
        return self.biaoji

    # 下面是调用摄像头
    def button_open_camera_clicked(self):
        # 改变界面显示状态
        if self.show_states == 0:
            self.set_new_states("0")
        else:
            self.set_new_states_two()
        self.is_starts = 1
        self.ser_new_opration("0")

        if not self.timer_camera.isActive():  # 若定时器未启动
            flag = self.cap.open(self.CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if not flag:  # flag表示open()成不成功
                msg = QtWidgets.QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.pushButton.setText('关闭会议')
        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.label.clear()  # 清空视频显示区域
            self.is_starts = 0
            self.show_states = 0
            self.pushButton.setText('开始会议')
            self.c_states.set_html_static_default(self.textBrowser_2)
            self.label.setText("<html><head/><body><p align=\"center\">显示摄像头</p></body></html>")

    def show_camera(self):
        self.image = self.show_img  # 从视频流中读取
        self.show = cv2.resize(self.image, (900, 680))  # 把读到的帧的大小重新设置
        self.show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        font = cv2.FONT_HERSHEY_SIMPLEX
        # self.set_number()
        font = cv2.FONT_HERSHEY_SIMPLEX
        if self.xy_number:
            self.show = self.set_number()

        showImage = QtGui.QImage(self.show.data, self.show.shape[1], self.show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    # 设置人的标识
    def set_number(self):
        font = cv2.FONT_HERSHEY_SIMPLEX

        self.xy_number = np.array(self.xy_number, dtype=np.int32)
        self.xy_number = self.xy_number.tolist()
        for i in range(0, self.person_number):
            self.show = cv2.putText(self.show, str(i), (int(self.xy_number[i][0]*0.7031), int(self.xy_number[i][1]*0.9444)), font, 1.2,
                                    (0, 0, 255), 2)
        return self.show

    def change_new_states_one(self):
        self.show_states = 0
        self.set_new_states(self.person_number)

    def change_new_states_two(self):
        self.show_states = 1
        self.set_new_states_two()

    def set_new_states(self, person_number):
        if person_number == 0 and self.show_states == 0:
            self.c_states.set_html0(self.textBrowser_2)
        elif person_number == 1 and self.show_states == 0:
            self.c_states.set_html1(self.textBrowser_2)
        elif person_number == 2 and self.show_states == 0:
            self.c_states.set_html2(self.textBrowser_2)
        elif person_number == 3 and self.show_states == 0:
            self.c_states.set_html3(self.textBrowser_2)

    def set_new_states_two(self):
        if self.is_starts == 1:
            self.c_states.set_html21(self.textBrowser_2)
        else:
            self.c_states.set_html22(self.textBrowser_2)

    def ser_new_opration(self, now_type):
        if now_type == "0":
            self.c_states.set_html10(self.textBrowser)
        elif now_type == "1":
            self.c_states.set_html11(self.textBrowser)
        elif now_type == "2":
            self.c_states.set_html12(self.textBrowser)
        elif now_type == "3":
            self.c_states.set_html13(self.textBrowser)
        elif now_type == "5":
            self.c_states.set_html14(self.textBrowser)
        elif now_type == "4":
            self.c_states.set_html15(self.textBrowser)
        elif now_type == "6":
            self.c_states.set_html16(self.textBrowser)

    def reImg(self, img):
        self.show_img = img

    # 下面是设置Log
    def set_Log(self, log, img):
        if self.mqtt.RevServer() and self.get_biaoji():
            print('收到远程控制')
            log = self.mqtt.RevServer()
            self.mqtt.mqtt.Rev = None
        self.json_str = json.loads(log)
        self.now_type = self.json_str["Hands_Pose"]["type"]  # 拿到操作
        self.hands_number = self.json_str["Hands_Pose"]["number"]  # 拿到编号
        self.person_number = self.json_str["Person"]["Number"]  # 拿到人数
        z = []
        for i in range(self.person_number):
            z.append(i)

        for i in range(self.person_number):  # 拿到人的坐标
            z[i] = [int((self.json_str["coordinate"]["x"][i][1] + self.json_str["coordinate"]["y"][i][1]) / 2),
                    int((self.json_str["coordinate"]["x"][i][0] + self.json_str["coordinate"]["y"][i][0]) / 2)]

        self.xy_number = z
        self.set_new_states(self.person_number)  # 更新状态
        self.ser_new_opration(self.hands_number)  # 更新动作
        self.action()  # 更新action
        self.action_win()
        if self.status:
            self.show = img
            self.set_number()  # 重新设置人的标识
        self.second_ui.set_person_number(self.person_number)
        # self.second_ui.show()  # 重新渲染
        self.mqtt.mqttKeep()
        
        # self.action_win()
        cv2.waitKey(5)

    # 进行具体操作
    def action(self):
        try:
            window = win32gui.GetClassName((win32gui.GetForegroundWindow()))
            if window == "PPTFrameClass" or window == "screenClass":
                self.action_off()
            elif window == "Qt5QWindowIcon" or window == "ApplicationFrameWindow":
                self.action_win()
        except BaseException:
            self.error = "当前窗口不是操作窗口"

    # ppt操作
    def action_off(self):

        if self.hands_number == "1":  # 点击

            self.c_off.open()
        elif self.hands_number == "2":  # 平移
            self.c_off.nextpage_off(1)
        elif self.hands_number == "3":  # 缩放
            self.c_off.close()
        elif self.hands_number == "5":  # 抓取
            self.c_off.translation_off()
        # elif self.person_numbe == "5":  # 旋转
        #     self.c_off.scaling_off()

    # 图片操作
    def action_win(self):

        if self.hands_number == "1":  # 点击s

            self.c_win.mouseclick(1)
        elif self.hands_number == "2":  # 平移
            self.c_win.nextpage_win(1)

        elif self.hands_number == "3":  # 缩放
            self.c_win.scaling_win(0)
        elif self.hands_number == "5":  # 抓取
            self.c_win.screen_shot()
            pass
        elif self.hands_number == "4":  # 旋转
            self.c_win.translation_win()
