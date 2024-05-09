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
    labels_list = []
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
        # print(objects)
        jixu = 0
        for obj_i in objects:
            label = obj_i['label']
            if label in out_classes:
                jixu = 1
        if jixu == 0:
            continue

        w = int(labelme_json['imageWidth'])
        h = int(labelme_json['imageHeight'])
        f = open("{}/{}".format(out_label_yolo, txt_name), "w")
        anquandai = np.zeros(11)
        no_anquandai = np.zeros(11)
        s = 0
        for obj_i in objects:
            n_s = 0

            label = obj_i['label']
            print(label)
            if label not in labels_list:
                labels_list.append(label)
            if label not in out_classes:
                continue

            print(obj_i)
            if label == '3' or label == '4':
                box = obj_i['points']

                x1, y1 = box[0]
                x2, y2 = box[1]

                x_min, y_min = min(x1, x2), min(y1, y2)
                x_max, y_max = max(x1, x2), max(y1, y2)

                cx, cy, b_w, b_h = xyxy2xywh([x_min, y_min, x_max, y_max])
                cx, cy, b_w, b_h = cx/w, cy/h, b_w/w, b_h/h

                cls_id = out_classes.index(label)

                if label == '3':
                    anquandai[:5] = cls_id, cx, cy, b_w, b_h
                    s = 1
                else:
                    no_anquandai[:5] = cls_id, cx, cy, b_w, b_h
                    n_s = 1
            if label == 'P0' or label == 'P1':
                p_box = obj_i['points']
                print(p_box)
                if label == 'P0':
                    px, py = p_box[0][0], p_box[0][1]
                    anquandai[5:8] = px/w, py/h, 2
                elif label == 'P1':
                    px, py = p_box[0][0], p_box[0][1]
                    anquandai[8:] = px/w, py/h, 2

            # if len(box) < 2:
            #     print(obj_i)
            #     a += 1
            #     print("num len(box) < 2 is {}".format(a))
            #     continue

            if n_s == 1:

                zero_out_no = no_anquandai.tolist()
                zero_out_no = str(zero_out_no)[1:-1].replace(", ", " ")

                f.write("{}\n".format(zero_out_no))

            if s == 1:
                zero_out = anquandai.tolist()
                zero_out = str(zero_out)[1:-1].replace(", ", " ")
                f.write("{}\n".format(zero_out))
                print(zero_out)
        f.close()
    print(labels_list)

if __name__ == '__main__':

    labelme_json_path = "/mnt/data1/zc_data/dianchang/dianchang_5yue/dianchang_all_0613_json_ori_7049"
    img_path = "/mnt/data1/zc_data/dianchang/dianchang_5yue/dianchang_all_0613_img_ori_7049_1280"
    out_label_yolo = "/mnt/data1/zc_data/dianchang/dianchang_5yue/aqd_pose_labels"




    # 所有数据类别
    # classes = ['person', 'hat', 'no_hat', 'safebelt', 'no_safebelt', 'uniform', 'no_uniform', 'Visitor_clothing',
    #            'fire_extinguisher', 'Fire extinguisher box', 'Inflammable_Materials', 'Fall_arrester', 'enclosure',
    #            'Handheld_items', 'hand']

    # out_classes = ['no_uniform', 'uniform', 'person', 'Visitor_clothing']
    out_classes = ['3', '4', 'P0', 'P1']
    # out_classes = ['安全带', '无安全带', '左挂钩', '右挂钩']
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

