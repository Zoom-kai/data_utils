# -*- coding=utf-8 -*-
# 工具类



import os
import random
import shutil
from shutil import copy2
import  argparse
import numpy as np
from tqdm import tqdm


def train_val_split(root_dir, train_percent):
    all_images = list(os.listdir(root_dir))
    np.random.shuffle(all_images)

    # train_data_path = os.path.join(root_dir, "train")
    val_data_path = os.path.join(root_dir, "val")

    # print(train_data_path, val_data_path)

    # exit()
    # if not os.path.exists(train_data_path):
    #     os.makedirs(train_data_path)
    if not os.path.exists(val_data_path):
        os.makedirs(val_data_path)
    #
    # if not os.path.exists(train_data_path.replace("images", "labels")):
    #     os.makedirs(train_data_path.replace("images", "labels"))
    # if not os.path.exists(val_data_path.replace("images", "labels")):
    #     os.makedirs(val_data_path.replace("images", "labels"))


    num_train = int(len(all_images) * train_percent)
    val_images = all_images[num_train:]
    train_images = all_images[:num_train]
    num = 0
    for img in tqdm(val_images):
        print(img)
        # if not os.path.exists(os.path.join(root_dir.replace("images", "labels"), img.replace("jpg", "txt"))):
        #     num +=1
        #     print("no label img number:{}".format(num))
        #     continue

        shutil.move(os.path.join(root_dir, img), val_data_path)
        # shutil.move(os.path.join(root_dir.replace("images", "labels"), img.replace("jpg", "txt")), val_data_path.replace("images", "labels"))

    # for img in tqdm(train_images):
    #     print(img)
    #     if not os.path.exists(os.path.join(root_dir.replace("images", "labels"), img.replace("jpg", "txt"))):
    #         num += 1
    #         print("no label img number:{}".format(num))
    #         continue
    #
    #     shutil.move(os.path.join(root_dir, img), train_data_path)
    #     shutil.move(os.path.join(root_dir.replace("images", "labels"), img.replace("jpg", "txt")),train_data_path.replace("images", "labels"))


if __name__ == '__main__':
    # VOC/images
    # VOC/labels

    parser = argparse.ArgumentParser()
    parser.add_argument('--root_path', type=str, default="/mnt/data3/zc_data/cls_16_data/resize_img/val_2_b", help='images dir')
    parser.add_argument('--train_percent', type=int, default=0.9, help='train_percent')
    args = parser.parse_args()

    root_path = args.root_path
    train_percent = args.train_percent

    train_val_split(root_path, train_percent)



