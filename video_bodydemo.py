# -------------------------------------#
#   调用摄像头或者视频进行检测
#   调用摄像头直接运行即可
#   调用视频可以将cv2.VideoCapture()指定路径
#   视频的保存并不难，可以百度一下看看
# -------------------------------------#
import time

import cv2
import numpy as np
from PIL import Image
import mediapipe as mp

from yolo import YOLO

yolo = YOLO()
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
# -------------------------------------#
#   调用摄像头
#   capture=cv2.VideoCapture("1.mp4")
# -------------------------------------#
with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as holistic:
    # capture = cv2.VideoCapture(0)
    capture = cv2.VideoCapture('C:\\Users\86151\Desktop\比赛资料\服创比赛说明材料\【A12】基于手势识别的会议控制系统【长安计算】-5 种基本动作示例视频\\2.平移.mp4')
    fps = 0.0
    while (True):
        t1 = time.time()
        # 读取某一帧
        ref, frame = capture.read()
        # 格式转变，BGRtoRGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # # 转变成Image
        frame = Image.fromarray(np.uint8(frame))
        # 进行检测
        frame = yolo.detect_image(frame)
        coordinates = frame[1]
        '''临时'''
        coordinates=coordinates[0][:]
        frame = np.array(frame[0])
        # RGBtoBGR满足opencv显示格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cropped = frame[int(coordinates[0]*1.04):int(coordinates[2]*0.99), int((coordinates[1])*0.52):int((coordinates[3])*1.18)]
        image = cv2.cvtColor(cv2.flip(cropped, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = holistic.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        fps = (fps + (1. / (time.time() - t1))) / 2
        # print("fps= %.2f" % (fps))
        image = cv2.putText(image, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("video", image)

        c = cv2.waitKey(1) & 0xff
        if c == ord('q'):
            capture.release()
            break

