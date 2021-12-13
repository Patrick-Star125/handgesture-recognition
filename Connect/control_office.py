import win32api
import win32con
from pykeyboard import *
from pymouse import *
import time


class control_office:
    def __init__(self):
        self.m = PyMouse()  # 鼠标对象
        self.k = PyKeyboard()  # 键盘对象

    # office缩放
    def translation_off(self):
        self.k.press_key(self.k.windows_l_key)
        self.k.press_key(0x2C)
        time.sleep(0.3)
        self.k.release_key(self.k.windows_l_key)
        self.k.release_key(0x2C)

    # office旋转
    def scaling_off(self):
        pass

    # office上/下一张图片（平移）
    def nextpage_off(self, code):
        time.sleep(0.5)
        if code == 0:
            self.n = 2
            self.mouseclick(3)
        elif code == 1:
            self.n = -2
            self.mouseclick(3)

    # 鼠标点击
    def mouseclick(self, code):
        x, y = self.m.position()
        if code == 1:
            self.m.click(x, y)  # 左
        elif code == 2:
            self.m.click(x, y, button=2)  # 右
        elif code == 3:
            # self.m.click(x, y, button=3, n=self.n)  # 中
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, self.n*200)

    # 打开ppt（点击）
    def open(self):

        self.k.press_key(0x74)
        time.sleep(0.5)
        self.k.release_key(0x74)

    # 关闭ppt（抓取）
    def close(self):
        self.k.press_key(0x1B)
        time.sleep(0.1)
        self.k.release_key(0x1B)