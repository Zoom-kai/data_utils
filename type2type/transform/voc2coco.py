# -*- coding=utf-8 -*-
#!/usr/bin/python

import argparse
import json
import os
import shutil
import sys
import xml.etree.ElementTree as ET

import numpy as np
# from tqdm import tqdm

START_BOUNDING_BOX_ID = 0
PRE_DEFINE_CATEGORIES = {}


def get(root, name):
    vars = root.findall(name)
    return vars


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError(
            'The size of %s is supposed to be %d, but is %d.' %
            (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def convert(xml_list, xml_dir, json_file):
    '''
    :param xml_list: 需要转换的XML文件列表
    :param xml_dir: XML的存储文件夹
    :param json_file: 导出json文件的路径
    :return: None
    '''
    list_fp = xml_list
    # 标注基本结构
    json_dict = {
        "type": "instances",
        "categories": [],
        "images": [],
        "annotations": []
    }

    print("\nfind images name")
    xml2img = dict()
    # for xml_file in xml_list:
    #     xml2img[xml_file] = None
        # for img_name in os.listdir(img_dir):
        #     if os.path.split(xml_file)[-1].split(".")[0] == img_name.split(".")[0]:
        #         xml2img[xml_file] = img_name
        #         continue

    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    image_id = 0

    print("\nparse xml annotations")
    for line in list_fp:
        print(f"processing {line}")
        filename = xml2img.get(line, None)
        # filename = line.split(".")[0]
        line = line.strip()
        # 解析XML
        xml_f = os.path.join(xml_dir, line)
        tree = ET.parse(xml_f)
        root = tree.getroot()
        path = get(root, 'path')
        # 取出图片名字
        if not filename:
            if len(path) == 1:
                filename = os.path.basename(path[0].text)
            elif len(path) == 0:
                filename = get_and_check(root, 'filename', 1).text
            else:
                raise NotImplementedError('%d paths found in %s' %
                                          (len(path), line))

        # shutil.copy(os.path.join(img_dir, filename),
        #             os.path.join(save_img_dir, filename))

        size = get_and_check(root, 'size', 1)
        # 图片的基本信息
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {
            'file_name': filename,
            'height': height,
            'width': width,
            'id': image_id
        }
        json_dict['images'].append(image)

        # 处理每个标注的检测框
        for obj in get(root, 'object'):
            # 取出检测框类别名称
            category = get_and_check(obj, 'name', 1).text
            print(22222222222222222222, category)
            # 更新类别ID字典
            if category not in categories:
                new_id = len(categories)
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(get_and_check(bndbox, 'xmin', 1).text) - 1
            ymin = int(get_and_check(bndbox, 'ymin', 1).text) - 1
            xmax = int(get_and_check(bndbox, 'xmax', 1).text)
            ymax = int(get_and_check(bndbox, 'ymax', 1).text)
            assert (xmax > xmin)
            assert (ymax > ymin)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            annotation = dict()
            annotation['id'] = bnd_id
            annotation['category_id'] = category_id
            annotation['image_id'] = image_id
            annotation['area'] = o_width * o_height
            annotation['bbox'] = [xmin, ymin, o_width, o_height]
            annotation['iscrowd'] = 0
            annotation['ignore'] = 0

            json_dict['annotations'].append(annotation)
            bnd_id = bnd_id + 1

        image_id += 1

    # 写入类别ID字典
    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    # 导出到json
    with open(json_file, 'w') as json_fp:
        json_str = json.dumps(json_dict, indent=4)
        json_fp.write(json_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', type=str, default=r"/mnt/data1/zc_data/da_model_merge/images/", help='images dir')   # 图片所在文件夹路径，后面的/一定要带上
    parser.add_argument('--xml_path', type=str, default=r"/mnt/data1/zc_data/da_model_merge/ceshi/", help='xml dir')      # xml文件路径，后面的/一定要带上
    parser.add_argument('--json_path', type=str, default=r"json/test111222.json", help='txt  dir')    # json文件保存路径

    args = parser.parse_args()

    img_path = args.img_path
    xml_path = args.xml_path
    json_path = args.json_path

    img_name = os.listdir(img_path)

    xml_labels = os.listdir(xml_path)
    json_file_dir = os.path.join(json_path, 'cocotype.json')

    convert(xml_labels, xml_path, json_path)

