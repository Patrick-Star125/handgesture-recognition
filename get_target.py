import numpy as np
import cv2


class Target(object):
    def __init__(self, coordinates):
        '''输入画面中检测框的坐标，初始化身份认证需要的所有属性'''
        self.image_points_y = []
        self.image_points_x = []
        for data in coordinates:
            self.image_points_y.append(int((data[0]+data[2])/2))
            self.image_points_x.append(int((data[1]+data[3])/2))
        self.now_points = {}
        self.now_points_xy = []
        self.thred = 300
        self.main_exist = 0
        self.frame_loss = 0
        self.lock = None
        self.near_m = None
        for i in range(len(self.image_points_x)):
            self.now_points_xy.append([self.image_points_x[i], self.image_points_y[i]])
            self.now_points[i] = self.now_points_xy[i]
        if len(self.image_points_x) == 1:
            self.main = dict(m=self.now_points_xy[0][:])
            self.main_exist = 1
        else:
            print("调用label来初始化一个m点")

    def update(self, coordinates):
        '''根据上一帧检测框的状态更新这一帧身份认证属性的值'''
        news_points = {}
        news_xy = []
        news_y = []
        news_x = []
        for data in coordinates:
            news_y.append(int((data[0]+data[2])/2))
            news_x.append(int((data[1]+data[3])/2))
        for i in range(len(news_x)):
            news_xy.append([news_x[i], news_y[i]])
            news_points[i] = news_xy[i]
        '''
        判断当画面内框的个数有无更新
        '''
        if len(news_x) == len(self.image_points_x):
            # 算距离,更新self.now_points为离上一帧self.now_points最近的点的坐标
            for i in range(len(news_x)):
                distance = self.now_points.copy()
                for j in range(len(news_x)):
                    distance[j] = ((news_xy[j][0] - self.now_points_xy[i][0]) ** 2 + (news_xy[j][1] - self.now_points_xy[i][1]) ** 2) ** 0.5
                self.now_points[i] = news_points[min(distance, key=distance.get)][:]
                self.now_points_xy = news_xy[:]

            if self.main_exist:
                # 算距离, 更新self.main为离上一帧self.now_points最近的点的坐标
                distance_m = self.now_points.copy()
                for i in range(len(news_x)):
                    distance_m[i] = ((self.main['m'][0] - news_xy[i][0]) ** 2 + ((self.main['m'][1] - news_xy[i][1]) ** 2)) ** 0.5
                # 只有m点的移动小于阈值，m点才会更新
                self.near_m=min(distance_m, key=distance_m.get)
                if distance_m[min(distance_m, key=distance_m.get)] <= self.thred:
                    self.main['m'] = news_points[min(distance_m, key=distance_m.get)][:]
                    self.frame_loss = 0
                else:
                    self.frame_loss += 1
                    print("这里丢了一帧")

        else:
            '''
            假如画面中前一帧和后一帧的框数量不一样
            '''
            self.image_points_y = news_y[:]
            self.image_points_x = news_x[:]
            self.now_points_xy = news_xy[:]
            self.now_points = news_points.copy()

    def label(self, num):
        '''输入数字，标记想要跟踪的那个人，被标记的那个人记为m'''
        if num in self.now_points is False:
            raise TypeError("该号数当前不存在")
        else:
            '''
            产生一个新的m点
            '''
            # self.now_points['m'] = self.now_points.pop(num)
            self.main = dict(m=self.now_points[num][:])
            self.main_exist = 1

    def ture_label(self, num):
        if num in self.now_points is False:
            self.lock = num
            self.main_exist = 1
        else:
            self.lock = num
            self.main = dict(m=self.now_points[num][:])
            self.main_exist = 1

    def keep_m(self):
        '''为m点的更新设定阈值，超过则判定m点丢失，需要重新启动m点'''
        if self.frame_loss >= 4:
            self.frame_loss = 0
            self.main_exist=0
            print("主体丢失，请重新确定主体")

    def draw_points(self, image):
        '''把所有画面中检测框的中心点，和m点，画出'''
        point_size = 1
        point_color = (0, 0, 255)
        thickness = 4

        points_list = []
        for i in range(len(self.image_points_x)):
            points_list.append(self.now_points[i])

        for points in points_list:
            cv2.circle(image, tuple(points), point_size, point_color, thickness)
            cv2.putText(image,'{}'.format(points_list.index(points)),tuple(points),cv2.FONT_HERSHEY_PLAIN,4,(0,255,0),4)

        if self.main_exist:
            cv2.circle(image, tuple(self.main['m']), point_size, (255, 0, 0), thickness)

        return image

    def __len__(self):
        '''对该类使用len()时返回点的数量'''
        return len(self.now_points_xy)




