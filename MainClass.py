import data_extraction
from CLient import client
from data import *
from ImageInterface import *
from get_target import Target
from label_list import Cutlist
import cv2 as cv
import mediapipe as mp
from multiprocessing import Queue

'''
     该文件用于定义手势识别应用程序类
     Application():
     ->  YOLO() //进行目标检测
     ->  Target() //标记目标
     ->  Characteristic() //进行特征点提取
     ->  classify()  //进程分类
'''


class Application:

    def __init__(self):

        self.list_cut = Cutlist(10, 10)
        self.test_base = 0
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.handspose = Hands()
        self.yolo = Yolodetection()
        self.connet = client()
        self.q = Queue(1)
        self.results = None
        self.show_frame = None
        self.coordinates = None
        self.yolodata = None
        self.image = None
        self.temp = None
        self.test = None
        self.Person = 0
        self.coordinate = None
        self.sendimg = None
        self.s = 0
        self.t = 0

    # 判断坐标是否存在
    def CoordinatesFlag(self) -> bool:
        try:
            self.coordinates = self.yolodata[1]
        except:
            return False
        return True

    # 获取标记特征点列表列表
    def GetList(self):
        temp = data_extraction.hands_to_list(self.results)
        now_xy = temp[:]
        now_xy = np.array(now_xy)
        now_xy = np.mean(now_xy, axis=1)
        right, left = now_xy[0], now_xy[1]
        hands_list = self.list_cut.videoStream(temp)
        image_list = self.handspose.image_cut.cameraStream(self.image)
        return hands_list, image_list, right, left

    # 目标检测
    def YOLO(self, frame):
        self.yolodata = self.yolo.YoloTreatment(frame)

    # 更新标记
    def UpPoints(self):
        self.coordinate = self.coordinates[:]
        num = self.connet.connect.getNum()
        upPoints(self.test_base, self.coordinate, self.test, num)

    # 标记目标
    async def Target(self):
        if self.test_base == 0:
            self.test = Target(self.coordinates)
        else:
            self.test.draw_points(self.show_frame)
            self.Person = len(self.coordinates)

            try:
                image = cv.cvtColor(self.image, cv.COLOR_RGB2BGR)
                self.UpPoints()
                return image
            except:
                print('Image obj is None ')
        self.test_base = 1

    # 获取特征点
    def Characteristic(self):

        if len(self.coordinates)>1:
            distance = []
            for i in self.coordinates:
                y=(int((i[0] + i[2]) / 2))
                x=(int((i[1] + i[3]) / 2))
                temp = ((self.test.main['m'][0] - x) ** 2 + ((self.test.main['m'][1] - y) ** 2)) ** 0.5
                distance.append(temp)
            index=distance.index(min(distance))
            self.coordinates = self.coordinates[index][:]
            # print("这里是俩个人")
        else:
            self.coordinates = self.coordinates[0][:]
            # print("这里是一个人")

        # print("coordinates_x:", int((self.coordinates[1] + self.coordinates[3]) / 2))
        # print("coordinates_y:", int((self.coordinates[0] + self.coordinates[2]) / 2))
        # if self.test.main_exist==1:
            # print("m点：", self.test.main)
        self.image = self.handspose.treatment(self.yolodata, self.coordinates)
        self.image.flags.writeable = False
        self.results = self.hands.process(self.image)
        # print("[info]:",self.s,self.results)
        if self.s == 0:
            self.cache = self.results
            self.s = 1
        self.image.flags.writeable = True

    # 进行分类
    def classify(self):
        hand_list, self.handspose.image_list, right, left = self.GetList()
        index = self.handspose.HandsClassification(hands_list=hand_list, righthand=right, lefthand=left)
        if index:
            res = IndexRecogniton(index, self.Person)
            log = ReadLog(self.coordinate)
            self.connet.Sendmsg(log)
            self.connet.ReLog(log, self.sendimg)
        # Classfication(self.handspose, self.GetList(), self.connet,self.Person,self.coordinate,self.sendimg)
