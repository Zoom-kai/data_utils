
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import sys
import argparse
import shutil

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
    num0 = 0
    num1 = 0
    num2 = 0
    num6 = 0
    num7 = 0

    # save_dir = "/mnt/data1/zc_data/data_da_model_2/jueyuanzi_b"
    for xml_name in xml_names:
        a, b, c, d, e = 0, 0, 0, 0, 0
        img_name = xml_name.replace(".xml", ".jpg")
        image_id = img_name[:-4]

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        in_file = open(xml_path + '/%s.xml' % (image_id), "r", encoding='utf-8')

        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        # cls_id = None

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in class_list:
                continue
            cls_id = class_list.index(cls)

            if cls_id == 0:
                a = 1

            elif cls_id == 1:
                b = 1
            elif cls_id == 2:
                c = 1
            elif cls_id == 6:
                d = 1
            elif cls_id == 7:
                e = 1

        if a == 1:
            num0 += 1
            print("num add 1, sum : {}".format(num0))
        elif b == 1:
            num1 += 1
            print("num1 add 1, sum : {}".format(num1))
        elif c == 1:
            num2 += 1
            print("num2 add 1, sum : {}".format(num2))
        elif d == 1:
            num6 += 1
            print("num6 add 1, sum : {}".format(num6))
        elif d == 1:
            num7 += 1
            print("num7 add 1, sum : {}".format(num7))

        # if num0 > 1000 and a==1:
        #     if os.path.exists(os.path.join(xml_path.replace("xml_labels", "images"), img_name)):
        #         shutil.move(os.path.join(xml_path.replace("xml_labels", "images"), img_name), save_dir)
        #     continue
        # elif num1 > 1000 and b==1:
        #     if os.path.exists(os.path.join(xml_path.replace("xml_labels", "images"), img_name)):
        #         shutil.move(os.path.join(xml_path.replace("xml_labels", "images"), img_name), save_dir)
        #     continue
        # elif num2 > 1000 and c==1:
        #     if os.path.exists(os.path.join(xml_path.replace("xml_labels", "images"), img_name)):
        #         shutil.move(os.path.join(xml_path.replace("xml_labels", "images"), img_name), save_dir)
        #     continue
        # elif num6 > 1000 and d==1:
        #     if os.path.exists(os.path.join(xml_path.replace("xml_labels", "images"), img_name)):
        #         shutil.move(os.path.join(xml_path.replace("xml_labels", "images"), img_name), save_dir)
        #     continue
        # elif num7 > 1000 and e==1:
        #     if os.path.exists(os.path.join(xml_path.replace("xml_labels", "images"), img_name)):
        #         shutil.move(os.path.join(xml_path.replace("xml_labels", "images"), img_name), save_dir)
        #     continue


        out_file = open(save_path + '/%s.txt' % (image_id), 'w')
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
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
    parser.add_argument('--xml_path', type=str, default=r"/mnt/data1/zc_data/fire_flash_yolo/fire_flash_0630/gdj/annotations", help='images dir')
    parser.add_argument('--txt_path', type=str, default=r"/mnt/data1/zc_data/fire_flash_yolo/fire_flash_0630/gdj/labels", help='xml files dir')
    # parser.add_argument('--classes', type=list, default=["02010002", "03011002", "03030002", "03030007", "07030001", "07030002", "07020002", "07020001", "03010002", "05010001"], help='xml files dir')
    parser.add_argument('--classes', type=list, default=["fire"])

    args = parser.parse_args()

    xml_path = args.xml_path
    txt_path = args.txt_path
    classes = args.classes

    convert_annotation(class_list=classes, xml_path=xml_path, save_path=txt_path)


