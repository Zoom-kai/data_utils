import xml
import os
import pandas as pd
import numpy as np
from shutil import copy
import cv2
import json


img_path = "/mnt/data1/zc_data/anquandai/ori_data/images"
save_path = "/mnt/data1/zc_data/anquandai/labels_ground"
new_img_path = "/mnt/data1/zc_data/anquandai/images_ground"

if not os.path.exists(save_path):
    os.makedirs(save_path)
if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)

df = pd.read_csv(r"/mnt/data1/zc_data/anquandai/ori_data/3train_rname.csv")
datas = df.values
# print(datas)

def compute_iou(rec_1, rec_2):
    '''
    rec_1:左上角(rec_1[0],rec_1[1])    右下角：(rec_1[2],rec_1[3])
    rec_2:左上角(rec_2[0],rec_2[1])    右下角：(rec_2[2],rec_2[3])
    （rec_1）
    1--------1
    1   1----1------1
    1---1----1      1
        1           1
        1-----------1 （rec_2）
    '''
    s_rec1 = (rec_1[2] - rec_1[0]) * (rec_1[3] - rec_1[1])  # 第一个bbox面积 = 长×宽
    s_rec2 = (rec_2[2] - rec_2[0]) * (rec_2[3] - rec_2[1])  # 第二个bbox面积 = 长×宽
    sum_s = s_rec1 + s_rec2  # 总面积
    left = max(rec_1[0], rec_2[0])  # 并集左上角顶点横坐标
    right = min(rec_1[2], rec_2[2])  # 并集右下角顶点横坐标
    bottom = max(rec_1[1], rec_2[1])  # 并集左上角顶点纵坐标
    top = min(rec_1[3], rec_2[3])  # 并集右下角顶点纵坐标
    if left >= right or top <= bottom:  # 不存在并集的情况
        return 0
    else:
        inter = (right - left) * (top - bottom)  # 求交集面积
        min_rec = min(s_rec1, s_rec2)  # 求两矩形较小面积
        iou = (inter / min_rec) * 1.0  # 计算IOU
        return iou

name_list = []
for data in datas:

    # print(data)
    name = data[4].split("/")[-1]
    objects = json.loads(data[5])["items"]
    label_name = name.split(".")[0]+".txt"

    f = open("{}/{}".format(save_path, label_name), "w")
    img = cv2.imread("{}/{}".format(img_path, name))
    h, w, c = img.shape
    a = 0
    boxes_0 = []
    boxes_1 = []
    boxes = []
    for object in objects:
        # print(object)
        box = object["meta"]["geometry"]
        class_label = object["labels"]["标签"]
        if class_label not in name_list:
            name_list.append(class_label)

        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        cls_id = name_list.index(class_label)



        if cls_id == 3:
            cls_id = 0
            boxes_0.append([cls_id, x1, y1, x2, y2])
        elif cls_id == 1:
            boxes_1.append([cls_id, x1, y1, x2, y2])

    for i, box_0 in enumerate(boxes_0):
        box0 = box_0[1:]
        boxes.append(box_0)
        for j, box_1 in enumerate(boxes_1):
            box1 = box_1[1:]
            iou = compute_iou(box0, box1)
            if iou > 0.2:
                print(iou)
                continue
            else:
                boxes.append(box_1)
    print(boxes)
    for [cls_id, x1, y1, x2, y2] in boxes:
        rec_w, rec_h = round((x2 - x1)/w, 2), round((y2 - y1)/h, 2)
        cx, cy = round(((x1 + x2)/w)/2, 2), round(((y1 + y2)/h)/2, 2)

        print(box, class_label, cls_id, cx, cy, rec_w, rec_h)
        f.write("{} {} {} {} {}\n".format(cls_id, cx, cy, rec_w, rec_h))

        cv2.imwrite("{}/{}".format(new_img_path, name), img)



    print(name_list)

    f.close()