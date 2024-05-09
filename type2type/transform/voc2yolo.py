
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
        print(xml_name, image_id)
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
            # difficult = obj.find('difficult').text
            cls = obj.find('name').text

            # if name != "green_net":
            #     # exit()
            # if name == "jueyuanzi":
            #     continue
            # if cls not in classes or int(difficult) == 1:
            #     print("cls {} not in classes !".format(cls))
            #     exit()
            #     continue
            print(cls, class_list)

            # if len(cls) < 3:
            #     cls_id = int(cls)
            # else:
            #     if cls not in class_list:
            #         continue
            #     cls_id = class_list.index(cls)
            if cls not in class_list:
                continue
            cls_id = class_list.index(cls)

            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_path', type=str, default=r"D:\BaiduNetdiskDownload\0609lvmo_biaozhu\annotations", help='images dir')
    parser.add_argument('--txt_path', type=str, default=r"D:\BaiduNetdiskDownload\0609lvmo_biaozhu\yololabels", help='xml files dir')

    parser.add_argument('--classes', type=str, default=r"D:\BaiduNetdiskDownload\0609lvmo_biaozhu\classes.txt"
    # ["aeroplane", "bicycle", "boat", "bus", "car", "motorbike", "train", "bottle", "chair", "diningtable", "pottedplant", "sofa", "tvmonitor", "bird", "cat", "cow", "dog", "horse", "sheep", "person"]
# ['fence', 'largemachinery']
                        , help='xml files dir')
    args = parser.parse_args()

    xml_path = args.xml_path
    txt_path = args.txt_path
    classes = args.classes
    f = open(args.classes, "r")
    # cls_list = []
    # classes_list = f.readlines()
    # print(classes_list)
    # for name in classes_list:
    #     print(name)
    #     name = name.strip("\n")
    #     cls_list.append(name)
    # print(cls_list)
    # exit()
    cls_list = ["绿膜"]
    convert_annotation(class_list=cls_list, xml_path=xml_path, save_path=txt_path)