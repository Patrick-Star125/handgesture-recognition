import json
import cv2 as cv
import numpy as np


'''
该文件用于定义一些判断函数，数据处理函数
'''



def SendLog(coordinate = None):
    data = {"Hands_Pose": {"type": "无", "number": "0"}, "Person": {"Number": 1},"coordinate": {"x": [[0,0]], "y": [[0,0]]}}

    if coordinate:

        coordinates = {"coordinate": {"x": None, "y": None}}
        x, y = [], []
        for i in range(len(coordinate)):

            x.append(coordinate[i][0:2])
            y.append(coordinate[i][2:4])
        x = np.array(x)
        y = np.array(y)
        x = x.astype(np.float).tolist()
        y = y.astype(np.float).tolist()

        coordinates["coordinate"]["x"] = x
        coordinates["coordinate"]["y"] = y

        data.update(coordinates)
        data["Person"]["Number"] = len(coordinate)

    data = json.dumps(data)
    return data


#双手判断
def Flags(flag)->bool:
    try:
        if len(flag) == 2:
            return True
    except:
        return False

#坐标点判断
def CoordinatesFlags(coordinates)->bool:

    if len(coordinates) == 0:
        return False
    for i in coordinates:
        if i == None:
            False

    return True

#分类结果转log数据
def Classfication(handspose,hands_list,c,Pum,coordinate,img):
    index = handspose.HandsClassification(hands_list)
    if index:
        res = IndexRecogniton(index,Pum)
        print(res)
        log = ReadLog(coordinate)
        c.ReLog(log,img)


#更新点的主体函数
def upPoints(test_base,coordinates,test,num):

    if test_base == 1:
        test.update(coordinates)
        if test.main_exist == 0:
            if num != None:
                test.ture_label(num)
            else:
                test.label(0)
        test.keep_m()



#将数据转成json，存入文件
def JsonTransform(Pose_name,index,P_num):

    data = {"type":Pose_name,"number":str(index)}
    Person = {"Number": P_num}
    hands = {"Hands_Pose":data,"Person":Person}
    jsonData = json.dumps(hands,ensure_ascii=False)
    with open('log.json','w+') as f:
        f.write(jsonData)
        f.close()
    res = (Pose_name,index)
    return res

#识别分类结果，返回log数据
def IndexRecogniton(index,Pum):
    Pose_name = '无'
    if index == 1:
        Pose_name = '点击'

    elif index == 2:
        Pose_name = '平移'

    elif index == 3:
        Pose_name = '缩放'

    elif index == 4:
        Pose_name = '旋转'

    elif index == 5:
        Pose_name = '抓取'

    elif index == 6:
        Pose_name = '无'
    else:
        index = 0


    log = JsonTransform(Pose_name,index,Pum)
    Pose_name, number = log

    return Pose_name+":"+str(number)

def tsleep(timeout)->bool:
    if timeout >= 1.8:
        return True
    else:
       return False


def ReadLog(coordinate):
    with open('log.json','r') as f:
        data = f.readline()
        data = json.loads(data)
        c = np.array(coordinate,dtype=np.float32)
        coordinate = c.tolist()
        length = data["Person"]["Number"]

        coordinates = {"coordinate": {"x": None, "y": None}}
        x,y =[],[]
        for i in range(length):
            x.append(coordinate[i][0:2])
            y.append(coordinate[i][2:4])

        coordinates["coordinate"]["x"] = x
        coordinates["coordinate"]["y"] = y
        data.update(coordinates)
        data = json.dumps(data)


        return data
