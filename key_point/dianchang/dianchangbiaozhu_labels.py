import json
import os
import numpy as np
import json
from glob import glob
import cv2
from sklearn.model_selection import train_test_split
from os import getcwd
from tqdm import tqdm

def xyxy2xywh(xyxy):
    x1, y1, x2, y2 = xyxy
    cx, cy = (x2+x1)/2, (y2+y1)/2
    w, h = x2-x1, y2-y1
    return [cx, cy, w, h]

def labelme_to_yolo(labelme_json_path, img_path, out_label_yolo):
    labelme_json_names = os.listdir(labelme_json_path)
    a = 0
    n = 0
    labels = []
    for name in tqdm(labelme_json_names):
        n += 1

        # if n < 4416:
        #     continue
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
        img_name = labelme_json['imagePath']
        if img_name.split('.')[-1] == 'gif':
            continue

        # print(os.path.join(img_path, img_name))
        if not os.path.exists(os.path.join(img_path, img_name)):
            # print(os.path.join(img_path, img_name))
            continue
        img = cv2.imread(os.path.join(img_path, img_name))
        # print(img)
        h, w, c = img.shape

        objects = labelme_json["shapes"]
        print(objects)
        jixu = 0
        for obj_i in objects:
            label = obj_i['value']
            if label not in labels:
                labels.append(label)

    print(labels)


if __name__ == '__main__':

    labelme_json_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/labels_json_0316"
    img_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/images"
    out_label_yolo = "/mnt/data1/zc_data/dianchang/dianchang_0308/aqd_pose/labels"

    # 所有数据类别
    classes = ['person', 'hat', 'no_hat', 'safebelt', 'no_safebelt', 'uniform', 'no_uniform', 'Visitor_clothing',
               'fire_extinguisher', 'Fire extinguisher box', 'Inflammable_Materials', 'Fall_arrester', 'enclosure',
               'Handheld_items', 'hand']

    # out_classes = ['no_uniform', 'uniform', 'person', 'Visitor_clothing']
    # out_classes = ['safebelt', 'no_safebelt', 'P1', 'P2']
    values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']

    # out_classes = ['safebelt', 'no_safebelt']
    # out_classes = ['person']

    # out_classes = ['Fall_arrester', 'Handheld_items', 'hand']
    # out_classes = ['fire_extinguisher', 'Fire extinguisher box', 'Inflammable_Materials']
    # 根据场景分类，需要输出的label类别

    # enclosure
    # out_classes = ['Fall_arrester', 'Handheld_items', 'hand']

    if not os.path.exists(out_label_yolo):
        os.makedirs(out_label_yolo)

    labelme_to_yolo(labelme_json_path, img_path, out_label_yolo)

