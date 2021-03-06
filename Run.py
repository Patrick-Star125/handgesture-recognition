from MainClass import Application
from data import *
import cv2 as cv
import time


import asyncio


async def main():
    #初始化应用
    app = Application()
    #初始化摄像头
    cap = app.connet.connect.get_cap()
    t = 0
    app.connet.MQTTClient()
    while 1:
        sart = time.time()
        ret ,frame = cap.read()
        if not ret:
            break
        app.sendimg, app.show_frame= frame.copy(), frame.copy()
        show = frame.copy()
        # 进行目标检测
        try:
            log = SendLog(app.coordinate)
        except:
            log = SendLog()
        app.connet.connect.set_Log(log, show)
        frame = cv.resize(frame, (1280 ,720))
        app.YOLO(frame)
        # 判断坐标是否存在
        if not app.CoordinatesFlag():
            continue
        # 判断坐标是否有效
        if not CoordinatesFlags(app.coordinates):
            continue
        # 标记主体
        await app.Target()
        # 取特征点
        app.Characteristic()
        # 判断是否为双手
        if not Flags(app.results.multi_hand_landmarks):
            continue
        # 手势识别分类
        app.classify()
        end = time.time()
        t += end-sart
        app.connet.MQTTKeep()
        # if t >= 2:
        #     print("[Info: 本次运行时间:%f]" % (end - sart))



asyncio.run(main())

















































































































































































































































































































































































































































































































































































































































































































































































