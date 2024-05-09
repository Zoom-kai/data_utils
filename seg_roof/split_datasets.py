# -*- coding=utf-8 -*-
# 工具类



import os
import random
import shutil
from shutil import copy2
import  argparse
import numpy as np
from tqdm import tqdm


def train_val_split(root_dir, train_percent, label_dir_name):
    all_images = list(os.listdir(root_dir))
    np.random.shuffle(all_images)

    train_data_path = os.path.join(root_dir, "train")
    val_data_path = os.path.join(root_dir, "val")

    print(train_data_path, val_data_path)

    # exit()
    if not os.path.exists(train_data_path):
        os.makedirs(train_data_path)
    if not os.path.exists(val_data_path):
        os.makedirs(val_data_path)

    if not os.path.exists(train_data_path.replace("images", label_dir_name)):
        os.makedirs(train_data_path.replace("images", label_dir_name))
    if not os.path.exists(val_data_path.replace("images", label_dir_name)):
        os.makedirs(val_data_path.replace("images", label_dir_name))


    num_train = int(len(all_images) * train_percent)
    val_images = all_images[num_train:]
    train_images = all_images[:num_train]
    num = 0
    for img in tqdm(val_images):
        print(img)
        if not os.path.exists(os.path.join(root_dir.replace("images", label_dir_name), img)):
            num +=1
            print("no label img number:{}".format(num))
            continue

        shutil.move(os.path.join(root_dir, img), val_data_path)
        shutil.move(os.path.join(root_dir.replace("images", label_dir_name), img), val_data_path.replace("images", label_dir_name))

    for img in tqdm(train_images):
        print(img)
        if not os.path.exists(os.path.join(root_dir.replace("images", label_dir_name), img)):
            num += 1
            print("no label img number:{}".format(num))
            continue

        shutil.move(os.path.join(root_dir, img), train_data_path)
        shutil.move(os.path.join(root_dir.replace("images", label_dir_name), img),train_data_path.replace("images", label_dir_name))


if __name__ == '__main__':
    # VOC/images
    # VOC/labels

    parser = argparse.ArgumentParser()
    parser.add_argument('--root_path', type=str, default="/mnt/data1/zc_data/map_data/train/images_png", help='images dir')
    parser.add_argument('--label_dir_name', type=str,
                        default="masks", help='label dir name')
    parser.add_argument('--train_percent', type=int, default=0.9, help='train_percent')
    args = parser.parse_args()

    root_path = args.root_path
    train_percent = args.train_percent
    label_dir_name = args.label_dir_name

    train_val_split(root_path, train_percent, label_dir_name)



