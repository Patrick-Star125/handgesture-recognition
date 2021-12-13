import time

import cv2
import numpy as np
from PIL import Image
import mediapipe as mp
from get_target import Target
from label_list import Cutlist

from yolo import YOLO
import data_extraction
from classification import Classification
import torch


def define_index(index, confidence, origin):
    name = ['点击','平移','缩放','旋转','抓取']
    if index == 0:
        print("{}，置信度为{}".format('点击', confidence))
    elif index == 1:
        print("{}，置信度为{}".format('平移', confidence))
    elif index == 2:
        print("{}，置信度为{}".format('缩放', confidence))
    elif index == 3:
        print("{}，置信度为{}".format('旋转', confidence))
    elif index == 4:
        print("{}，置信度为{}".format('抓取', confidence))
    elif index ==5:
        print('无[{}],置信度为{}'.format(name[origin],confidence))


def filter(index, confidence, index_list, confidence_list):
    '''index_list的长度待定'''
    num = np.zeros(5)
    for i in index_list:
        num[i] += 1

    if index == 0:
        if ((confidence>=0.25 and confidence<=0.70) or (confidence>=0.72 and confidence<=0.96)) and (num[1]>=1 or num[2]>=1 or num[4] >=1):
            return index
    if index == 1:
        if ((confidence>=0.26 and confidence<=0.70) or (confidence>=0.70 and confidence<=0.865)) and (num[2]>=1,num[3]):
            return index
    if index == 2:
        if ((confidence>=0.26 and confidence<=0.51) or (confidence>=0.51 and confidence<=0.68) or (confidence>=0.7 and confidence<=0.87) or (confidence>=0.87 and confidence<=0.97)):
            return index
    if index == 3:
        if ((confidence>=0.32 and confidence<=0.76) or (confidence>=0.82 and confidence<=0.90)) and (num[1]>=1 or num[2]>=1) or num[4]>=1:
            return index
    if index == 4:
        # if ((confidence>=0.32 and confidence <=0.45) or (confidence >=0.8 and confidence <=0.85) or (confidence >=0.512 and confidence <=0.61)) and (num[3]>=1 or num[0]>=1 or num[1]>=1):
        if ((confidence >= 0.33 and confidence <= 0.61) or (confidence >= 0.67 and confidence <= 0.85)) and (num[3] >= 1 or num[0] >= 1 or num[1] >= 1):
            return index

    return 5

def pause(index,t1):
    '定为1.5秒'
    pa = 1
    t2 = time.time() - t1
    if t2<=1.50:
        index = 5
        return index,pa
    else:
        print('冷却时间结束')
        pa = 0
        return index,pa

def hands_to_center(index, righthand, lefthand):
    if index == 5:
        return index
    elif index == 0:
        # or (((lefthand[0] > 0.5 and righthand[0] > 0.5) or (lefthand[0] < 0.5 and righthand[0] < 0.5)) and (lefthand[1] > 0.5 and righthand[1] > 0.5))
        # and ((lefthand[1] > 0.5 and righthand[1] < 0.5) or (lefthand[1] < 0.5 and righthand[1] > 0.5))
        if (((lefthand[0] > 0.5 and righthand[0] < 0.5) or (lefthand[0] < 0.5 and righthand[0] > 0.5)) and ((lefthand[1] > 0.5 and righthand[1] < 0.5) or (lefthand[1] < 0.5 and righthand[1] > 0.5)) and ((lefthand[1]-righthand[1]>0.3) or (righthand[1]-lefthand[1]>0.3))):
            print('点击：',"right_x:%.2f" % righthand[0], "right_y:%.2f" % righthand[1], "left_x:%.2f" % lefthand[0],"left_y:%.2f" % lefthand[1])
            return index
        if  (righthand[1]>0.5 and lefthand[1]>0.5) and ((lefthand[0]>0.5 and righthand[0]>0.5) or (lefthand[0]<0.5 and righthand[0]<0.5)):
            print('点击转平移:',"right_x:%.2f" % righthand[0], "right_y:%.2f" % righthand[1], "left_x:%.2f" % lefthand[0],"left_y:%.2f" % lefthand[1])
            return 1
        else: return 5
    elif index == 4:
        if ((lefthand[0] > 0.5 and righthand[0] < 0.5) or (lefthand[0] < 0.5 and righthand[0] > 0.5)) and ((lefthand[1]>0.5 and righthand[1]<0.5) or (lefthand[1]<0.5 and righthand[1]>0.5)):
            print('抓取：', "right_x:%.2f" % righthand[0], "right_y:%.2f" % righthand[1], "left_x:%.2f" % lefthand[0],"left_y:%.2f" % lefthand[1])
            return index
        else: return 5

    elif index == 1:
        if (lefthand[1] > 0.5 and righthand[1] > 0.5):
            # and ((lefthand[1] - righthand[1]) > 0.1 or (righthand[1] - lefthand[1]) > 0.1)
            if (((lefthand[0]-righthand[0]) < 0.32) and ((righthand[0]-lefthand[0]) < 0.32)):
                print('平移：', "right_x:%.2f" % righthand[0], "right_y:%.2f" % righthand[1], "left_x:%.2f" % lefthand[0],"left_y:%.2f" % lefthand[1])
                return index
        else: return 5

    elif index == 2:
        if (lefthand[1] > 0.5 and righthand[1] > 0.5):
            if ((((lefthand[0]-righthand[0]) < 0.36) and ((righthand[0]-lefthand[0]) < 0.36)) or ((lefthand[0]-righthand[0]>0.68) or ((righthand[0]-lefthand[0])>0.68))) and ((lefthand[1]-righthand[1]<0.1) and (righthand[1]-lefthand[1]<0.1)):
                print('缩放：', "right_x:%.2f" % righthand[0], "right_y:%.2f" % righthand[1], "left_x:%.2f" % lefthand[0], "left_y:%.2f" % lefthand[1])
                return index
        else: return 5

    elif index == 3:
        if ((lefthand[1]>0.42 and righthand[1]<0.42) or (lefthand[1]<0.42 and righthand[1]>0.42)) and (((lefthand[0]-righthand[0]) < 0.3) and (righthand[0]-lefthand[0]) < 0.3):
            print('旋转：', "right_x:%.2f" % righthand[0], "right_y:%.2f" % righthand[1], "left_x:%.2f" % lefthand[0],"left_y:%.2f" % lefthand[1])
            return index
        else: return 5

    return 5


def DataPretreatment(annotations):
    temp = np.array(annotations)
    temp = temp.reshape(10, 2, 7, 3, 2)
    temp = np.mean(temp, axis=3)
    shape = temp.shape
    temp = temp.reshape(shape[0] * shape[1] * shape[2] * shape[3])
    result = temp.tolist()

    return result


def visual_dataset(imagelist):
    # for image in imagelist:
    #     cv2.imshow("video", image)
    #     c = cv2.waitKey(1) & 0xff
    head = imagelist[-1]
    last = imagelist[0]
    cv2.imshow('video1', head)
    cv2.imshow('video2', last)
    c = cv2.waitKey(1) & 0xff


def rotate(loadpath, savepath):
    '''将平移数据集增强为两种动作'''
    num_mp4 = 37
    while (num_mp4):
        capture = cv2.VideoCapture(loadpath + '\\{}.mp4'.format(num_mp4))
        width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        saver = cv2.VideoWriter(savepath + '\\{}.avi'.format(num_mp4), fourcc, 30.0, (int(width), int(height)), True)
        while (capture.isOpened()):
            ret, frame = capture.read()
            if ret == True:
                frame = cv2.flip(frame, 1)
                saver.write(frame)
            else:
                break
        num_mp4 -= 1


def video_to_label(file_path, label, all_avi):
    list_cut = Cutlist(10, 10)
    image_cut = Cutlist(10, 10)
    index_cut = Cutlist(2, 2)
    confidence_cut = Cutlist(2, 2)
    num_avi = 1
    s = 0
    pa = 0
    index_cache = None
    yolo = YOLO()
    classify = Classification()
    mp_hands = mp.solutions.hands
    '''临时'''
    mp_drawing = mp.solutions.drawing_utils
    while (1):
        with mp_hands.Hands(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            if num_avi > all_avi:
                break
            capture = cv2.VideoCapture(file_path + '\\{}.mp4'.format(num_avi))
            # capture = cv2.VideoCapture(file_path)
            #capture = cv2.VideoCapture(0)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            while (1):
                ret, frame = capture.read()
                # cv2.imshow('image',frame)
                # if not ret:
                #     '''这里有改动'''
                #     via_list = list_cut.cameraStream(10, via_list)
                #     via_image = image_cut.cameraStream(10, via_image)
                #     break
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(np.uint8(frame))
                frame = yolo.detect_image(frame)
                try:
                    coordinates = frame[1]
                except:
                    print('这一帧没检测到人')
                    continue
                if len(coordinates) == 0:
                    print('这一帧没检测到人')
                    continue
                for i in coordinates:
                    if i == None:
                        print('这一帧里有坐标None')
                        continue
                coordinates = coordinates[0][:]
                frame = np.array(frame[0])
                # RGBtoBGR满足opencv显示格式
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                # 对框的大小进行微调，保证手在框中，而检测框在输入图像外
                cropped = frame[int(coordinates[0] * 1.0):int(coordinates[2] * 1.2),
                          int((coordinates[1]) * 0.85):int((coordinates[3]) * 1.15)]
                image = cv2.cvtColor(cv2.flip(cropped, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)

                if s == 0:

                    cache = results

                    s = 1
                image.flags.writeable = True
                if results.multi_hand_landmarks is None:
                    continue

                if len(results.multi_hand_landmarks) != 2:
                    results = cache
                else:
                    cache = results
                '''画图测试'''

                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                temp = data_extraction.hands_to_list(results)
                '''temp入队'''
                hand_list = list_cut.cameraStream(temp)
                image_list = image_cut.cameraStream(image)
                if hand_list is not None:
                    try:
                        hand_result = DataPretreatment(hand_list[::-1])
                    except:
                        continue
                    results = classify.predict(hand_result, 'num_1_batch_1_lr_0.0001_ep_12.pth')
                    result = torch.max(results, dim=0)
                    confidence = result.values.data.tolist()
                    index = result[1].tolist()
                    if image_list is not None:
                        visual_dataset(image_list)
                    '''用index缓冲'''
                    if index_cache == None:
                        index_cache = index
                    print('[info]:cache%d---index=%d' % (index_cache, index))
                    if index == index_cache:
                        continue
                    else:

                        index_list = index_cut.cameraStream(index_cache)
                        index_cache = index
                    if pa == 1:
                        index, pa = pause(index, t1)
                    print(index_list)
                    confidence_list = confidence_cut.cameraStream(confidence)
                    if index_list is None or len(index_list) != 2:
                        continue
                    print(index_list)
                    index = filter(index, confidence, index_list, confidence_list)
                    if index != 5:
                        pa = 1
                        t1=time.time()
                    define_index(index, confidence,index_cache)

