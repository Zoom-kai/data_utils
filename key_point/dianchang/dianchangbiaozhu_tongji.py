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
    n_box = 0
    labelme_json_names = os.listdir(labelme_json_path)
    a = 0
    n = 0
    for name in tqdm(labelme_json_names):
        n += 1
        # if n < 4556:
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


        objects = labelme_json["shapes"]
        print(objects)
        # w = int(labelme_json['imageWidth'])
        # h = int(labelme_json['imageHeight'])
        f = open("{}/{}".format(out_label_yolo, txt_name), "w")

        for obj_i in objects:
            # label = obj_i['value']
            box = obj_i['points']
            if len(box) > 2:
                n_box += 1

            print("n_box : ", n_box)
    print(n_box)

if __name__ == '__main__':

    # labelme_json_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/labels_json_0316"
    # img_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/images"
    # out_label_yolo = "/mnt/data1/zc_data/dianchang/dianchang_0308/person_yolo"

    labelme_json_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/ori_data/biaozhu/jiaoshoujia"  #"/mnt/data1/zc_data/dianchang/dianchang_0308/labels_json_0316"
    # /mnt/data1/zc_data/dianchang/dianchang_0308/ori_data/biaozhu/biaozhu_buchong

    # labelme_json_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/ori_data/biaozhu/biaozhu_buchong/all"

    img_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/images"
    out_label_yolo = "/mnt/data1/zc_data/dianchang/dianchang_0308/yanshou"


    # 所有数据类别
    classes = ['person', 'hat', 'no_hat', 'safebelt', 'no_safebelt', 'uniform', 'no_uniform', 'Visitor_clothing',
               'fire_extinguisher', 'Fire extinguisher box', 'Inflammable_Materials', 'Fall_arrester', 'enclosure',
               'Handheld_items', 'hand']

    # out_classes = ['no_uniform', 'uniform', 'person', 'Visitor_clothing']
    # out_classes = ['no_hat', 'hat']
    # out_classes = ['safebelt', 'no_safebelt']
    # out_classes = ['person']

    # out_classes = ['Fall_arrester', 'Handheld_items', 'hand']
    # out_classes = ['fire_extinguisher', 'Fire extinguisher box', 'Inflammable_Materials']
    # 根据场景分类，需要输出的label类别
    out_classes = ['Fall_arrester', 'Fire11111111111', '1111111111111111']
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

