from abc import ABCMeta, abstractmethod
from classification import *
from generate_dataset import *
from yolo import YOLO
from PIL import Image
import cv2 as cv
import numpy as np

'''
该文件用于定义一些算法的接口类
'''


# 接口定义
class interface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def treatment(self):
        pass


# 抽象类定义
class FramePretreatment(interface):

    @abstractmethod
    def treatment(self):
        pass


# 目标价检测类定义
class Yolodetection(FramePretreatment):

    def __init__(self):
        self.yolo = YOLO()

    # 进行图像预处理
    def treatment(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = Image.fromarray(np.uint8(frame))

        return frame

    # 目标检测、获取yolo处理的图像数据
    def YoloTreatment(self, frame):
        frame = self.treatment(frame)
        yolo_data = self.yolo.detect_image(frame)

        return yolo_data


# 手势分类的类
class Hands(FramePretreatment):

    def __init__(self):
        self.confidence_cut = Cutlist(2, 2)
        self.index_cut = Cutlist(2, 2)
        self.image_cut = Cutlist(10, 10)
        self.cla = Classification()
        self.hand_result = []
        self.image_list = None
        self.index_cache = None
        self.pa = 0
        self.t1 = None

    # 进行图像处理，标记特征点
    def treatment(self, frame, coordinates):

        frame = np.array(frame[0])
        # RGBtoBGR满足opencv显示格式
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        # 对框的大小进行微调，保证手在框中，而检测框在输入图像外
        cropped = frame[int(coordinates[0] * 0.9):int(coordinates[2] * 1.2),
                  int((coordinates[1]) * 0.9):int((coordinates[3]) * 1.2)]
        image = cv.cvtColor(cv.flip(cropped, 1), cv.COLOR_BGR2RGB)

        return image

    # 进行对分类数据预处理
    def DataPretreatment(self, annotations):
        temp = np.array(annotations)
        temp = temp.reshape(10, 2, 7, 3, 2)
        temp = np.mean(temp, axis=3)
        shape = temp.shape
        temp = temp.reshape(shape[0] * shape[1] * shape[2] * shape[3])
        result = temp.tolist()

        return result

    # 手势分类算法入口，返回分类结果
    def HandsClassification(self, hands_list, righthand, lefthand):
        if hands_list is not None:
            self.hand_result = self.DataPretreatment(hands_list)

            # 模型调用
            result = self.cla.predict(self.hand_result, 'num_1_batch_1_lr_0.0001_ep_12.pth')
            result = torch.max(result, dim=0)
            confidence = result.values.data.tolist()
            index = result[1].tolist()

            # if self.image_list is not None:
            #     visual_dataset(self.image_list)

            if self.index_cache == None:
                self.index_cache = index

            if index == self.index_cache:
                return 0
                pass
            else:
                index_list = self.index_cut.cameraStream(self.index_cache)
                self.index_cache = index

            if self.pa == 1:
                index, self.pa = pause(index, self.t1)

            print(index_list)
            confidence_list = self.confidence_cut.cameraStream(confidence)
            if index_list is None or len(index_list) != 2:
                return 0
                pass
            else:
                index = filter(index, confidence, index_list, confidence_list)
                if index == None:
                    a = 1
                index = hands_to_center(index, righthand, lefthand)
                if index == None:
                    a = 1
                if index != 5:
                    self.pa = 1
                    self.t1 = time.time()
                if index==5:
                    print('无：', "right_x:%.2f" % righthand[0], "right_y:%.2f" % righthand[1], "left_x:%.2f" % lefthand[0], "left_y:%.2f" % lefthand[1])
                define_index(index, confidence, self.index_cache)


            return index + 1
