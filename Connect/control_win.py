import time
import numpy as np
from PIL import ImageGrab
import win32api
import win32con
import win32gui
from PyQt5.QtWidgets import QApplication
import  cv2 as cv

from pykeyboard import *
from pymouse import *
import Connect.shot


class control_win:
    def __init__(self):
        self.hwnd_title = dict()
        self.m = PyMouse()  # 鼠标对象
        self.k = PyKeyboard()  # 键盘对象

    # win10旋转
    def translation_win(self):
        self.k.press_key(0x11)
        self.k.press_key(0x52)
        time.sleep(0.2)
        self.k.release_key(0x11)
        self.k.release_key(0x52)

    # win10缩放
    def scaling_win(self, code):

        if code == 0:
            self.n = 2
            self.mouseclick(3)
        elif code == 1:
            self.n = -2
            self.mouseclick(3)

    # win10上/下一张图片(平移)
    def nextpage_win(self, code):
        if code == 0:
            # time.sleep(5)
            # self.k.press_key(0x11)
            # time.sleep(0.3)
            # win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 1)
            # time.sleep(0.3)
            # self.k.release_key(0x11)
            self.k.press_key(0x25)
            time.sleep(0.3)
            self.k.release_key(0x25)
        elif code == 1:
            # time.sleep(3)
            # self.k.press_key(0x11)
            # time.sleep(0.3)
            # win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1)
            # time.sleep(0.3)
            # self.k.release_key(0x11)
            self.k.press_key(0x27)
            time.sleep(0.3)
            self.k.release_key(0x27)
            print('平移')

    # 鼠标点击
    def mouseclick(self, code):
        x, y = self.m.position()
        if code == 1:
            self.m.click(x, y)  # 左
        elif code == 2:
            self.m.click(x, y, button=2)  # 右
        elif code == 3:
            self.m.click(x, y, button=3, n=self.n)  # 中
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, self.n*200)

    # 截图（抓取）
    def screen_shot(self):
        self.k.press_key(self.k.windows_l_key)
        self.k.press_key(0x2C)
        time.sleep(0.3)
        self.k.release_key(self.k.windows_l_key)
        self.k.release_key(0x2C)

