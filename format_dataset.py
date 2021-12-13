import scipy.io as scio
import cv2
import PIL as Image
import mediapipe as mp
import torch
import numpy as np


# a = scio.loadmat("D:\Dataset\Hand_Dataset\hand_dataset\\training_dataset\\training_data\\annotations\Buffy_17.mat")
# b = list(a['boxes'])
# c = cv2.imread("D:\Dataset\Hand_Dataset\hand_dataset\\training_dataset\\training_data\images\Buffy_17.jpg")
# x1 = b[0][1][0][0][0].tolist()
# x2 = b[0][1][0][0][1].tolist()
# x3 = b[0][1][0][0][2].tolist()
# x4 = b[0][1][0][0][3].tolist()
# A = tuple(list(map(int, x1[0])))
# B = tuple(list(map(int, x2[0])))
# C = tuple(list(map(int, x3[0])))
# D = tuple(list(map(int, x4[0])))
# # print(b)
# c = cv2.putText(c, "A", A, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
# c = cv2.putText(c, "B", B, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
# c = cv2.putText(c, "C", C, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
# c = cv2.putText(c, "D", D, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
# cv2.line(c, A, B, (255, 0, 0), 1, cv2.LINE_4)
# cv2.line(c, A, D, (255, 0, 0), 1, cv2.LINE_4)
# cv2.line(c, B, C, (255, 0, 0), 1, cv2.LINE_4)
# cv2.line(c, C, D, (255, 0, 0), 1, cv2.LINE_4)
# cv2.imshow('image', c)
# k = cv2.waitKey(0)
# if k == ord("q"):
#     cv2.destroyWindow("image")


class Posture(object):
    def __init__(self, videopath='./video', mode='cam'):
        mp_drawing = mp.solutions.drawing_utils
        mp_holistic = mp.solutions.holistic

        if mode == 'cam':
            cap = cv2.VideoCapture(0)
        if mode == 'vid':
            cap = cv2.VideoCapture(videopath)
        with mp_holistic.Holistic(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as holistic:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # Flip the image horizontally for a later selfie-view display, and convert
                # the BGR image to RGB.
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                results = holistic.process(image)

                # Draw landmark annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # mp_drawing.draw_landmarks(
                #     image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
                mp_drawing.draw_landmarks(
                    image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                mp_drawing.draw_landmarks(
                    image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                cv2.imshow('MediaPipe Holistic', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()


class Hands(object):
    def __init__(self, videopath, mode='cam'):
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands

        if mode == 'cam':
            cap = cv2.VideoCapture(0)
        if mode == 'vid':
            cap = cv2.VideoCapture(videopath)
        with mp_hands.Hands(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # Flip the image horizontally for a later selfie-view display, and convert
                # the BGR image to RGB.
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(50) & 0xFF == 27:
                    break
        cap.release()

# capture = cv2.VideoCapture(0)
# capture = cv2.VideoCapture('C:\\Users\86151\Desktop\比赛资料\服创比赛说明材料\【A12】基于手势识别的会议控制系统【长安计算】-5 种基本动作示例视频\\2.平移.mp4')
# pthfile = './model_data/yolov4_tiny_weights_coco.pth'
# net = torch.load(pthfile)
# for key, value in net:
#     print(key, value, sep=' ')
a=Hands(videopath='C:\\Users\86151\Desktop\比赛资料\服创比赛说明材料\【A12】基于手势识别的会议控制系统【长安计算】-5 种基本动作示例视频\\2.平移.mp4',mode='vid')




