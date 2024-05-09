import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import sys
import cv2
import argparse
from tqdm import tqdm
# -*- coding=utf-8 -*-
import numpy as np


def drow_box(img_dir_path, txt_dir_path, savepath):
    image_id = 0
    txt_names = os.listdir(txt_dir_path)
    n = 0
    print(txt_names)
    np.random.shuffle(txt_names)
    for txt_name in tqdm(txt_names):

        n += 1
        if n > 500:
            break
        img_name = txt_name.replace(".txt", ".jpeg")
        image_id = img_name[:-4]
        img_path = "{}/{}".format(img_dir_path, img_name)
        txt_path = "{}/{}".format(txt_dir_path, txt_name)
            # print(img_path)
            # print(image_id)
        # else:
        #     continue
        txt_file = open(txt_path, "r")
        if not os.path.exists(img_path):
            continue

        img = cv2.imread(img_path)
        lines = txt_file.readlines()

        # print(lines)

        img_h = img.shape[0]
        img_w = img.shape[1]
        for line in lines:
            line = line.split()
            print(line)
            if line == []:
                continue
            cx, cy, w, h = float(line[1])*img_w, float(line[2])*img_h, float(line[3])*img_w, float(line[4])*img_h
            x1, y1, x2, y2 = cx-0.5*w, cy-0.5*h, cx + 0.5*w, cy + 0.5*h

            cls = line[0]
            print(cls)
            # if cls == 2:
            #     print("Missing_pin")

            # cls = "Pin"
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(img, cls, (int(x1+20), int(y1+20)), font, fontScale=1,color= (0, 255, 0), thickness=2)
            # print((int(x1), int(y1)), (int(x2), int(y2)))
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 2)

        if not os.path.isdir(savepath):
            os.makedirs(savepath)

        print(img)
        print("{}/{}.jpg".format(savepath, image_id))
        cv2.imwrite("{}/{}.jpg".format(savepath, image_id), img)

        txt_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--txt_path', type=str, default=r"/mnt/data3/zc_data/jx_0217/original/lvmo_05_data/labels", help='txt files dir')
    parser.add_argument('--img_path', type=str, default=r"/mnt/data3/zc_data/jx_0217/original/lvmo_05_data/images", help='img files dir')
    parser.add_argument('--save_path', type=str, default=r"/mnt/data3/zc_data/jx_0217/original/lvmo_05_data/images/preview_val_0607", help='draw rectangle to picture')

    args = parser.parse_args()

    txt_path = args.txt_path
    img_path = args.img_path
    save_path = args.save_path
    print(1111111111)

    drow_box(img_path, txt_path, save_path)
    print(22222222222)


