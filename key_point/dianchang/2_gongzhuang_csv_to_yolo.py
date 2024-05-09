import xml
import os
import pandas as pd
import numpy as np
from shutil import copy
import cv2
import json


img_path = "/mnt/data1/zc_data/open_source_biandianzhan/gongzhuangshibie/ori_data/2_images"
save_path = "/mnt/data1/zc_data/open_source_biandianzhan/gongzhuangshibie/labels"
img_new_path = "/mnt/data1/zc_data/open_source_biandianzhan/gongzhuangshibie/images"
if not os.path.exists(save_path):
    os.makedirs(save_path)

df = pd.read_csv(r"/mnt/data1/zc_data/open_source_biandianzhan/gongzhuangshibie/ori_data/2train_rname.csv")
datas = df.values
# print(datas)

name_list = []
for data in datas:

    # print(data)
    name = data[4].split("/")[-1]
    objects = json.loads(data[5])["items"]
    # print(objects)
    label_name = name.split(".")[0]+".txt"

    f = open("{}/{}".format(save_path, label_name), "w")
    img = cv2.imread("{}/{}".format(img_path, name))
    h, w, c = img.shape
    for object in objects:
        print(object)
        box = object["meta"]["geometry"]
        class_label = object["labels"]["标签"]
        if class_label not in name_list:
            name_list.append(class_label)

        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        rec_w, rec_h = round((x2 - x1)/w, 2), round((y2 - y1)/h, 2)
        cx, cy = round(((x1 + x2)/w)/2, 2), round(((y1 + y2)/h)/2, 2)
        cls_id = name_list.index(class_label)

        if int(cls_id) == 0:
            continue
        if int(cls_id) == 3:
            cls_id = 0
        print(box, class_label, cls_id, cx, cy, rec_w, rec_h)
        f.write("{} {} {} {} {}\n".format(cls_id, cx, cy, rec_w, rec_h))
    print(name_list)

    f.close()


