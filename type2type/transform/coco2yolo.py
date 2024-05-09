# -*- coding=utf-8 -*-

"""
author: Wu
https://github.com/Weifeng-Chen/DL_tools/issues/3
2021/1/24
COCO 格式的数据集转化为 YOLO 格式的数据集，源代码采取遍历方式，太慢，
这里改进了一下时间复杂度，从O(nm)改为O(n+m)，但是牺牲了一些内存占用
--json_path 输入的json文件路径
--save_path 保存的文件夹名字，默认为当前目录下的labels。
"""

import os
import json
from tqdm import tqdm
import argparse


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = box[0] + box[2] / 2.0
    y = box[1] + box[3] / 2.0
    w = box[2]
    h = box[3]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def coco2yolo(json_file, ana_txt_save_path):
    data = json.load(open(json_file, 'r'))
    if not os.path.exists(ana_txt_save_path):
        os.makedirs(ana_txt_save_path)

    id_map = {}  # coco数据集的id不连续！重新映射一下再输出！
    # for i, category in enumerate(data['categories']):
    #     # print(category)
    #     # print(id_map, category['id'])
    #
    #     id_map[int(category['id'])] = i+1

    # 通过事先建表来降低时间复杂度
    max_id = 0
    for img in data['images']:
        max_id = max(max_id, img['id'])
    # 注意这里不能写作 [[]]*(max_id+1)，否则列表内的空列表共享地址
    img_ann_dict = [[] for i in range(max_id + 1)]
    for i, ann in enumerate(data['annotations']):
        img_ann_dict[ann['image_id']].append(i)

    for img in tqdm(data['images']):
        filename = img["file_name"]
        img_width = img["width"]
        img_height = img["height"]
        img_id = img["id"]
        # print(1111111111111, filename)
        head, tail = os.path.splitext(filename)
        ana_txt_name = head + ".txt"  # 对应的txt名字，与jpg一致
        f_txt = open(os.path.join(ana_txt_save_path, ana_txt_name), 'w')
        '''for ann in data['annotations']:
            if ann['image_id'] == img_id:
                box = convert((img_width, img_height), ann["bbox"])
                f_txt.write("%s %s %s %s %s\n" % (id_map[ann["category_id"]], box[0], box[1], box[2], box[3]))'''
        # 这里可以直接查表而无需重复遍历
        for ann_id in img_ann_dict[img_id]:
            ann = data['annotations'][ann_id]

            # box = convert((img_width, img_height), ann["bbox"])

            box = ann["bbox"]
            dw = 1. / (img_width)
            dh = 1. / (img_height)
            x = box[0] + box[2] / 2.0
            y = box[1] + box[3] / 2.0
            w = box[2]
            h = box[3]

            x = x * dw
            w = w * dw
            y = y * dh
            h = h * dh
            print(id_map, ann["category_id"])
            if ann["category_id"] >= 2:
                print(222222222, img)
            f_txt.write("%s %s %s %s %s\n" % (ann["category_id"], x, y, w, h))
            #f_txt.write("%s %s %s %s %s\n" % (id_map[ann["category_id"]], x, y, w, h))
        f_txt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_path', default=r'/mnt/data1/zc_data/tswitch/longhua/longhua_tswitch2/longhua2.json', type=str,       # json文件保存路径
                        help="input: coco format(json)")
    parser.add_argument('--save_path', default=r'/mnt/data1/zc_data/tswitch/longhua/longhua_tswitch2/labels', type=str,               # txt文件保存路径
                        help="specify where to save the output dir of labels")
    arg = parser.parse_args()

    json_file = arg.json_path  # COCO Object Instance 类型的标注
    ana_txt_save_path = arg.save_path  # 保存的路径

    coco2yolo(json_file, ana_txt_save_path)

