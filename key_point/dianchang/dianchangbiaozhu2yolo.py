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
        # print(objects)
        w = int(labelme_json['imageWidth'])
        h = int(labelme_json['imageHeight'])
        f = open("{}/{}".format(out_label_yolo, txt_name), "w")
        for obj_i in objects:
            label = obj_i['value']
            box = obj_i['points']
            if label not in out_classes:
                print(label)
                continue

            # print(obj_i)
            if len(box) < 2:
                print(obj_i)
                a += 1
                print("num len(box) < 2 is {}".format(a))
                continue
            x1, y1 = box[0]
            x2, y2 = box[1]

            x_min, y_min = min(x1, x2), min(y1, y2)
            x_max, y_max = max(x1, x2), max(y1, y2)

            cx, cy, b_w, b_h = xyxy2xywh([x_min, y_min, x_max, y_max])
            cx, cy, b_w, b_h = cx/w, cy/h, b_w/w, b_h/h

            cls_id = out_classes.index(label)

            if cls_id == 2:
                cls_id = 0
            f.write("{} {} {} {} {}\n".format(cls_id, cx, cy, b_w, b_h))

        f.close()
        if not os.path.getsize("{}/{}".format(out_label_yolo, txt_name)):
            os.remove("{}/{}".format(out_label_yolo, txt_name))

if __name__ == '__main__':
    #
    # labelme_json_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/labels_json_0316"
    # img_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/images"
    # out_label_yolo = "/mnt/data1/zc_data/dianchang/dianchang_0308/person_yolo"

    labelme_json_path = "/mnt/data1/zc_data/dianchang/dianchang_7yue_dk/data_jlw/json_labels"
    img_path = "/mnt/data1/zc_data/dianchang/dianchang_7yue_dk/data_jlw/images"
    out_label_yolo = "/mnt/data1/zc_data/dianchang/dianchang_7yue_dk/data_jlw/labels_shouchi_jlw"


    # 所有数据类别
    classes = ['person', 'hat', 'no_hat', 'safebelt', 'no_safebelt', 'uniform', 'no_uniform', 'Visitor_clothing',
               'fire_extinguisher', 'Fire extinguisher box', 'Inflammable_Materials', 'Fall_arrester', 'enclosure',
               'Handheld_items', 'hand']

    out_classes = ['13', '14']
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

