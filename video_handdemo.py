# -------------------------------------#
'''数据集可视化文件'''
# -------------------------------------#
import time

import cv2
import numpy as np
from PIL import Image
import mediapipe as mp
from get_target import Target

from yolo import YOLO
import data_extraction

yolo = YOLO()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# -------------------------------------#
#   调用摄像头
#   capture=cv2.VideoCapture("1.mp4")
# -------------------------------------#
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    # capture = cv2.VideoCapture(0)
    capture = cv2.VideoCapture(0)
    fps = 0.0
    test_base=0
    while (True):
        t1 = time.time()
        # 读取某一帧
        ref, frame = capture.read()
        # 格式转变，BGRtoRGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        '''临时'''
        show_frame=frame.copy()
        # # 转变成Image
        frame = Image.fromarray(np.uint8(frame))
        # 进行检测
        frame = yolo.detect_image(frame)

        coordinates = frame[1]
        # 当没有检测到图片内有人时，跳过这一帧
        if len(coordinates) == 0:
            continue
        # 当coordinate中出现None时，跳过这一帧
        for i in coordinates:
            if i==None:
                continue
        print(coordinates)
        '''临时'''
        if test_base==0:
            test = Target(coordinates)
        if test_base==1:
            test.update(coordinates)
            if test.main_exist==0:
                test.label(0)
            test.keep_m()
            test.draw_points(show_frame)
        test_base=1
        coordinates=coordinates[0][:]
        frame = np.array(frame[0])
        # RGBtoBGR满足opencv显示格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # 对框的大小进行微调，保证手在框中，而检测框在输入图像外
        cropped = frame[int(coordinates[0]*1.04):int(coordinates[2]*0.99), int((coordinates[1])*0.52):int((coordinates[3])*1.18)]
        image = cv2.cvtColor(cv2.flip(cropped, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        '''临时'''
        show_frame=cv2.cvtColor(show_frame,cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)


        fps = (fps + (1. / (time.time() - t1))) / 2
        # print("fps= %.2f" % (fps))
        image = cv2.putText(image, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        '''临时'''
        cv2.imshow('show', show_frame)
        cv2.imshow("video", image)

        c = cv2.waitKey(100) & 0xff
        if c == ord('q'):
            capture.release()
            break

