import abc
import cv2 as cv

'''
buffer类
video_cut类
'''


class Buffer:
    '''
        创建队列--传入队列长度
    '''

    def __init__(self, length):
        self.len = length
        self.q = []
        self.number = 0
        self.count = 0

    # 判断为空
    def isempty(self):
        if self.q == []:
            return 1
        else:
            return 0

    # 判断是否满
    def isfull(self):
        if self.number == self.len:
            return 1
        else:
            return 0

    # 入队
    def enqueue(self, elem):
        if self.isfull():
            pass
        else:
            self.number += 1
            self.q.append(elem)

    # 出队
    def dequeue(self, index, flag=False):
        if self.isempty():
            return 0
        else:
            self.number -= 1
            if flag == False:
                return self.q.pop(0)
            else:
                try:
                    val = self.q[index]
                    self.count += 1
                    return val
                except:
                    return 0

    # 读取缓存最早图片
    '''
        读取缓冲区数据，index--索引，flag--True，根据索引取数，False，从队头取数
    '''

    def readBuffer(self, index, flag):
        val = self.dequeue(index, flag)
        return val

    # 读取缓存区图片
    '''
        返回整个队列
    '''

    def readBuffers(self):
        return self.q

    # 清理缓存
    '''
        队列清除
    '''

    def clearBuffer(self):
        self.number = 0
        self.q.clear()
        return self.q

    # 存入图片
    '''
        数据入队
    '''

    def writeBuffer(self, elem):
        self.enqueue(elem)


class Video_cut:
    '''
    初始化传参,video_path--视频路径，frameRate--帧数间隔，blen--缓冲区长度，flag--是否按间隔取帧,True--按间隔取,count--要取的帧数
    单独使用摄像头时只需要令video_path=0,传入frameRate和count两个参数即可
    '''

    def __init__(self, video_path, frameRate=1, blen=30, count=10, flag=False):
        self.frameRate = frameRate
        self.path = video_path
        print('[frameRate]:帧数间隔为%d' % frameRate)
        self.blen = blen
        self.count = count
        self.buf = Buffer(self.blen)
        self.img_buf = []
        self.ret = 1
        self.flag = flag

    '''对传入路径的视频进行间隔取帧处理，返回一个队列'''

    def videoStream(self):
        if self.path == 0:
            print('非视频路径')
            exit()

        fcount = 0
        self.cap = cv.VideoCapture(self.path)
        ret, first = self.cap.read()
        # 读取第一帧，如果视频不存在则退出
        if ret:
            self.ret = 1
            if not self.buf.len == 0:
                print('[buffer]:缓冲区成功创建，长度为%d' % self.blen)
            else:
                print('长度不能为0')
        else:
            self.ret = 0
            print('视频不存在')

        '''循环对视频进行读取'''
        while True and self.ret:
            ret, frame = self.cap.read()

            # 视频读取完毕将缓冲区剩下的图片按间隔取出
            if not ret:
                others_len = self.buf.number
                for i in range(0, others_len, self.frameRate):
                    if len(self.img_buf) < self.count:
                        self.img_buf.append(self.buf.readBuffer(i, self.flag))

                self.buf.clearBuffer()
                break

            # 缓冲区则将图片放入列表
            fcount += 1
            if self.buf.isfull():

                for i in range(0, self.blen, self.frameRate):
                    if len(self.img_buf) < self.count:
                        print("取走第%d帧" % i)
                        self.img_buf.append(self.buf.readBuffer(i, self.flag))

                if not self.img_buf == []:
                    print('取走的帧数:%d,buf剩余图片:%d' % (self.buf.count, self.buf.number))
                self.buf.clearBuffer()

            # 存入缓冲区
            else:
                self.buf.writeBuffer(frame)
                print("存入帧数%d" % self.buf.number)
            cv.imshow('frame',frame)

        if self.img_buf == []:
            print('存储错误')
            exit()
        return self.img_buf

    '''
        摄像头进行间隔取帧
    '''
    def c_cap(self):
        if not self.path==0:
            print("非摄像头打开方式")
            exit()

        self.cap = cv.VideoCapture(self.path)
        fcount = 0
        fnum = 0
        img_list = []
        while True:
            ret ,frame = self.cap.read()
            if not ret:
                print('摄像头出现问题')
                break

            if fcount < self.count and fnum % self.frameRate==0:
                img_list.append(frame)
                fcount += 1
            fnum += 1

            if fcount == self.count:
                break

        print("取出帧数：%d"%len(img_list))
        return img_list




path = 0
video = Video_cut(video_path=path, frameRate=3, blen=20, count=10, flag=True)
img_list = video.c_cap()
print(len(img_list))
# ipath = "d:\\cap\\buf\\"
#
# for i,img in enumerate(img_list):
#     img_path = ipath + str(i) + ".jpg"
#
#     cv.imwrite(img_path,img)
