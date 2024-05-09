
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import sys
import argparse
from tqdm import tqdm

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


def convert_annotation(class_list, xml_path, save_path):
    xml_names = os.listdir(xml_path)

    for xml_name in tqdm(xml_names):
        img_name = xml_name.replace(".xml", ".jpg")
        image_id = img_name[:-4]

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        in_file = open(xml_path + '/%s.xml' % (image_id), "r", encoding='utf-8')
        out_file = open(save_path + '/%s.txt' % (image_id), 'w')
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
            # print(cls, class_list)
            cls_id = class_list.index(cls)

            if cls_id > 1:
                cls_id = 1
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_path', type=str, default=r"/mnt/data1/zc_data/anquandai/ground_or/20230403爬高477/annotations", help='images dir')
    parser.add_argument('--txt_path', type=str, default=r"/mnt/data1/zc_data/anquandai/ground_or/20230403爬高477/yolo_labels", help='xml files dir')
    parser.add_argument('--classes', type=list, default=['DSFPP', 'KZFPP', 'KZPP'], help='xml files dir')
    args = parser.parse_args()

    xml_path = args.xml_path
    txt_path = args.txt_path
    classes = args.classes

    convert_annotation(class_list=classes, xml_path=xml_path, save_path=txt_path)
