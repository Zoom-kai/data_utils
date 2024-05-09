import json
import os
import numpy as np
import json
from glob import glob
import cv2
from sklearn.model_selection import train_test_split
from os import getcwd
from tqdm import tqdm

import shapely
import shapely.geometry

def xyxy2xywh(xyxy):
    x1, y1, x2, y2 = xyxy
    cx, cy = (x2+x1)/2, (y2+y1)/2
    w, h = x2-x1, y2-y1
    return [cx, cy, w, h]

def sort_corners(box):
    # “”“将四个角点按顺时针方向排序”“”
    # 将坐标原点移至重心
    box_float = box.astype(float)
    center = np.mean(box_float, 0)
    centered = box_float - center
    # 计算每个顶点的极角
    print(centered[:, 1], centered[:, 0], 33333333333333333333)
    angles = np.arctan2(centered[:, 1], centered[:, 0])
    # 按顺时针方向排序
    sort_idxs = np.argsort(angles)
    sorted_points = box[sort_idxs, :]
    # 返回结果
    return sorted_points

oneD2twoD = lambda x: [(x[2 * i], x[2 * i + 1]) for i in
                       range(len(x) // 2)]  # one D [x, y, x, y, x, y, ...] to [(x, y), (x, y), ...]


def polygon_to_rect_coord(polygon_coord):
    polygon_coord = np.array(polygon_coord, np.int32)
    print(polygon_coord)
    segment = polygon_coord.flatten().tolist()
    segment = oneD2twoD(segment + segment[:2])
    multipoint = shapely.geometry.MultiPoint(segment)
    # try:
    print(segment)
    # if len(segment==3):

    label = np.array(multipoint.minimum_rotated_rectangle.exterior.coords[:-1]).ravel().tolist()

    # rect = cv2.minAreaRect(polygon_coord)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)

    # sorted_box = sort_corners(box)
    # # rect = cv2.minAreaRect(polygon_coord)

    # 逼近多边形顶点的轮廓，得到近似四边形的顶点坐标
    # epsilon = 0.02 * cv2.arcLength(polygon_coord, True)
    # approx = cv2.approxPolyDP(polygon_coord, epsilon, True)
    # 对四个角点排序

    # sorted_box = sort_corners(approx)

    return label

def bbox_to_rect_coord(x1, y1, x2, y2):
    # 左上角 p1
    p1 = (x1, y1)
    # 右上角 p2
    p2 = (x2, y1)
    # 右下角 p3
    p3 = (x2, y2)
    # 左下角 p4
    p4 = (x1, y2)
    # 将点按照顺时针方向排列
    # rect_coord = [p1, p2, p3, p4, p1]

    return x1, y1, x2, y1, x2, y2, x1, y2

def labelme_to_yolo(labelme_json_path, img_path, out_label_yolo):
    labelme_json_names = os.listdir(labelme_json_path)
    a = 0
    n = 0
    for name in tqdm(labelme_json_names):
        n += 1

        if n == 4557:
            continue

        # print(name)
        json_name = name
        if not name.split('.')[-1] == 'json':
            continue
        name = name.split('.')[0]

        # img_name = name+'.jpg'

        txt_name = name+'.txt'

        # lines = f.readlines()
        # print(lines[1:])
        f = open((os.path.join(labelme_json_path, json_name)), "r", encoding="utf-8")
        labelme_json = json.loads(f.read())
        # img_name = labelme_json['imagePath']
        img_name = name + ".png"
        if img_name.split('.')[-1] == 'gif':
            continue
        print(222222222)
        # print(os.path.join(img_path, img_name))
        # if not os.path.exists(os.path.exists(os.path.join(img_path, img_name))):
        #     # print(os.path.join(img_path, img_name))
        #     continue
        # img = cv2.imread(os.path.join(img_path, img_name))
        # # print(img)
        # h, w, c = img.shape

        objects = labelme_json["shapes"]
        # print(objects)
        w = int(labelme_json['imageWidth'])
        h = int(labelme_json['imageHeight'])
        f = open("{}/{}".format(out_label_yolo, txt_name), "w")
        for obj_i in objects:
            label = obj_i['label']
            box = obj_i['points']
            print(box)
            if label == 0:
                x1, y1 = box[0]
                x2, y2 = box[1]
                box_4 = bbox_to_rect_coord(x1, y1, x2, y2)
            else:
                if len(box) == 2:
                    x1, y1 = box[0]
                    x2, y2 = box[1]
                    box_4 = bbox_to_rect_coord(x1, y1, x2, y2)
                else:
                    box_4 = polygon_to_rect_coord(box)


            if label not in out_classes:
                print(label)
                continue

            # print(obj_i)
            # if len(box) < 2:
            #     print(obj_i)
            #     a += 1
            #     print("num len(box) < 2 is {}".format(a))
            #     continue
            x1, y1, x2, y2, x3, y3, x4, y4 = box_4


            cls_id = out_classes.index(label)

            f.write("{} {} {} {} {} {} {} {} {} {} \n".format(x1, y1, x2, y2, x3, y3, x4, y4, cls_id, 0))

        f.close()


if __name__ == '__main__':
    #
    # labelme_json_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/labels_json_0316"
    # img_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/images"
    # out_label_yolo = "/mnt/data1/zc_data/dianchang/dianchang_0308/person_yolo"

    labelme_json_path = "/mnt/data1/zc_data/dianchang/jsj_0602/json_labels"
    img_path = "/mnt/data1/zc_data/dianchang/jsj_0602/images_ori"
    out_label_yolo = "/mnt/data1/zc_data/dianchang/jsj_0602/labels"


    # 所有数据类别
    classes = ['person', 'hat', 'no_hat', 'safebelt', 'no_safebelt', 'uniform', 'no_uniform', 'Visitor_clothing',
               'fire_extinguisher', 'Fire extinguisher box', 'Inflammable_Materials', 'Fall_arrester', 'enclosure',
               'Handheld_items', 'hand']

    out_classes = ['0', '2', "1"]
    # out_classes = ['no_hat', 'hat']
    # out_classes = ['safebelt', 'no_safebelt']
    # out_classes = ['person']

    # out_classes = ['Fall_arrester', 'Handheld_items', 'hand']
    # out_classes = ['fire_extinguisher', 'Fire extinguisher box', 'Inflammable_Materials']
    # 根据场景分类，需要输出的label类别
    # out_classes = ['Fall_arrester', 'Fire11111111111', '1111111111111111']
    # enclosure
    # out_classes = ['Fall_arrester', 'Handheld_items', 'hand']
    # out_classes = ['Fall_arrester', 'Handheld_items', 'hand']
    # out_classes = ['fire_extinguisher', 'Fire extinguisher box', 'Inflammable_Materials']

    # 根据场景分类，需要输出的label类别

    # enclosure
    # out_classes = ['Fall_arrester', 'Handheld_items', 'hand']

    if not os.path.exists(out_label_yolo):
        os.makedirs(out_label_yolo)

    labelme_to_yolo(labelme_json_path, img_path, out_label_yolo)

