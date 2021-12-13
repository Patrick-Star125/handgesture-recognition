import cv2 as cv
import abc
import numpy as np


class Buffer:
    def __init__(self, length):
        self.len = length
        self.q = []
        self.number = 0
        self.count = 0

    def isempty(self):
        if self.q == []:
            return 1
        else:
            return 0

    def isfull(self):
        if self.number == self.len:
            return 1
        else:
            return 0

    def enqueue(self, elem):
        if self.isfull():
            pass
        else:
            self.number += 1
            self.q.append(elem)

    def dequeue(self, index, step=True):
        if self.isempty():
            return 0
        else:
            self.number -= 1
            if step == True:
                return self.q[0]
            else:
                try:
                    val = self.q[index]
                    self.count += 1
                    return val
                except:
                    return 0

    # 读取缓存最早图片
    def readBuffer(self, index, step):
        val = self.dequeue(index, step)
        return val

    # 读取缓存区图片
    def readBuffers(self):
        return self.q

    # 清理缓存
    def clearBuffer(self):
        self.number = 0
        self.q.clear()
        return self.q

    # 存入图片
    def writeBuffer(self, elem):
        self.enqueue(elem)


class Cut(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def videoStream(self):
        pass


class Video_cut(Cut):
    def __init__(self, video_path, frameRate=1, blen=30):
        self.frameRate = frameRate
        print('[frameRate]:帧数间隔为%d' % frameRate)
        self.blen = blen
        self.buf = Buffer(self.blen)
        self.img_buf = []
        self.cap = cv.VideoCapture(video_path)
        ret, first = self.cap.read()
        if ret:
            if not self.buf.len == 0:
                print('[buffer]:缓冲区成功创建，长度为%d' % self.buf.len)
            else:
                print('长度不能为0')
        else:
            print('视频不存在')

    def videoStream(self, step=True):

        while True:
            ret, frame = self.cap.read()
            if not ret:
                others_len = self.buf.number
                for i in range(0, others_len, self.frameRate):
                    self.img_buf.append(self.buf.readBuffer(i, step))
                self.buf.clearBuffer()
                break

            if self.buf.isfull():
                for i in range(0, self.blen, self.frameRate):
                    print("取走第%d帧" % i)
                    self.img_buf.append(self.buf.readBuffer(i, step))
                if not self.img_buf == []:
                    print('取走的帧数:%d,buf剩余图片:%d' % (self.buf.count, self.buf.number))
                self.buf.clearBuffer()

            else:
                self.buf.writeBuffer(frame)
                print("存入帧数%d" % self.buf.number)

        return self.img_buf


'''
    用于存放列表数据
    实例化需要传入需要的长度
'''


class Cutlist(Cut):
    def __init__(self, length, get_num):
        # self.vlist = np.array(vlist,ndmin=1)
        self.len = length
        self.num = get_num
        self.count = 0
        self.l = []

    # 列表为满的判断
    def is_full(self):
        if self.count == self.len:
            return 1
        return 0

    # 清空列表
    def lclear(self):
        self.l.clear
        self.count = 0

        # --------------------------#
        #    参数为要传入的列表数据
        #  返回值为存放列表数据的列表
        # --------------------------#

    def videoStream(self, vlist):
        self.re_l = []
        if not self.is_full():
            self.l.append(vlist)
            self.count += 1
            # if self.count == self.len:
            #     return self.l

            print('缓冲')
            return None

        self.l.pop(0)
        self.l.append(vlist)
        for i in range(0, self.len, int(self.len / self.num)):
            self.re_l.append(self.l[i])
        return self.re_l

    def cameraStream(self, vlist):
        self.re_l = []
        if not self.is_full():
            self.l.append(vlist)
            self.count += 1
            # if self.count == self.len:
            #     return self.l

            print('缓冲')
            return None

        self.l.pop(0)
        self.l.append(vlist)
        for i in range(0, self.len, int(self.len / self.num)):
            self.re_l.append(self.l[i])
        return self.re_l

