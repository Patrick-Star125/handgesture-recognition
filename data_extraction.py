import numpy as np
import mediapipe as mp


def hands_to_list(handness):
    '''把手的坐标提取为列表'''
    two_hands = []
    for hand_landmarks in handness.multi_hand_landmarks:
        one_hand = []
        for i in range(21):
            x = hand_landmarks.landmark.__getitem__(i).x
            y = hand_landmarks.landmark.__getitem__(i).y
            xy = [x, y]
            one_hand.append(xy)
        one_hand.sort()
        two_hands.append(one_hand)

    return two_hands


def to_annotation(label, hands, width, height):
    '''将坐标list转化为训练和推理所需的数据'''
    annotations = []
    for hand in hands:
        annotation = hands_to_list(hand, width, height)
        annotation = np.array(annotation).reshape(84)
        annotations.append(list(annotation))

    annotations = list(np.array(annotations).reshape(len(hands) * 84))

    return annotations.append(label)


def annotation_to_file(path, annotations):
    '''将带有label的annotation存入txt文件中'''
    label = annotations[-1]
    temp = np.array(annotations[:-1])

    shape = temp.shape
    temp = temp.reshape(shape[0] * shape[1] * shape[2] * shape[3])
    temp = temp.tolist()

    ann_txt = open(path, 'a+')
    ann_str = str(temp)
    # temp1 = ann_str.strip('[')
    # temp2 = temp1.strip(']')
    temp1 = ann_str.replace('[', '')
    temp2 = temp1.replace(']', '')
    temp3 = temp2.replace(' ', '')
    temp4 = temp3 + ',' + str(label)
    ann_txt.writelines(temp4)
    ann_txt.write('\n')
    print('成功载入一条数据集')
