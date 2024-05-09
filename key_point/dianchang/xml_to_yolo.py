
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import sys
import argparse
from tqdm import tqdm
from shutil import copy

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(class_list, xml_path, save_path, img_path = None, new_img_path=None):
    xml_names = os.listdir(xml_path)

    for xml_name in tqdm(xml_names):
        img_name = xml_name.replace(".xml", ".jpg")
        image_id = img_name[:-4]
        a = 0
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        if not os.path.exists(new_img_path):
            os.makedirs(new_img_path)
        in_file = open(xml_path + '/%s.xml' % (image_id), "r", encoding='utf-8')

        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            # if cls not in classes or int(difficult) == 1:
            #     print("cls {} not in classes !".format(cls))
            #     exit()
            #     continue
            print(cls, class_list)
            if cls not in class_list:
                continue
            else:
                a += 1
        if a == 0:
            continue
        out_file = open(save_path + '/%s.txt' % (image_id), 'w')
        copy(img_path + '/%s.jpg' % (image_id), new_img_path)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            # if cls not in classes or int(difficult) == 1:
            #     print("cls {} not in classes !".format(cls))
            #     exit()
            #     continue
            print(cls, class_list)
            if cls not in class_list:
                continue
            print(cls, 11111111)
            cls_id = class_list.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            print(b)
            bb = convert((w, h), b)
            print(str(cls_id) + " " + " ".join([str(a) for a in bb]), '/%s.txt' % (image_id))
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        out_file.close()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_path', type=str, default=r"/mnt/data1/zc_data/fire_flash_yolo/fire_voc_2012/voc2012_fire/fire_data/voc_labels/", help='images dir')
    parser.add_argument('--txt_path', type=str, default=r"/mnt/data1/zc_data/fire_flash_yolo/fire_voc_2012/voc2012_fire/fire_data/yolo_labels/", help='xml files dir')
    parser.add_argument('--img_path', type=str, default=r"/mnt/data1/zc_data/fire_flash_yolo/fire_voc_2012/voc2012_fire/fire_data/images/", help='xml files dir')
    parser.add_argument('--new_img_path', type=str, default=r"/mnt/data1/zc_data/open_source_biandianzhan/images/test", help='xml files dir')
    parser.add_argument('--classes', type=list, default=
    # ["aeroplane", "bicycle", "boat", "bus", "car", "motorbike", "train", "bottle", "chair", "diningtable", "pottedplant", "sofa", "tvmonitor", "bird", "cat", "cow", "dog", "horse", "sheep", "person"]
['fire']
                        , help='xml files dir')
    args = parser.parse_args()

    xml_path = args.xml_path
    txt_path = args.txt_path
    classes = args.classes
    img_path = args.img_path
    new_img_path = args.new_img_path

    convert_annotation(class_list=classes, xml_path=xml_path, save_path=txt_path, img_path = img_path, new_img_path=new_img_path)