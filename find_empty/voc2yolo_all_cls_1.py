
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
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_path', type=str, default=r"/mnt/data1/zc_data/da_model_merge/xml_labels", help='images dir')
    parser.add_argument('--txt_path', type=str, default=r"/mnt/data1/zc_data/da_model_merge/yolo_labels", help='xml files dir')
    parser.add_argument('--classes', type=list, default=['02010001', '02013001', '02010002', '02010006', '02010004', '02010005', '02020001', '02020003', '02020004', '02030001', '02030002', '03010001', '03010002', '03011002', '03010003', '03013001', '03020001', '03020003', '03021002', '03030001', '03030002', '03030003', '03030004', '03030006', '03030005', '03030007', '03040001', '03040002', '03040003', '03040005', '03040007', '03040008', '03040009', '03040010', '03040011', '03040012', '03040013', '03040014', '03040015', '03040016', '03040017', '03040018', '03040023', '03040024', '03040025', '03050002', '03051001', '03052001', '03060001', '03060002', '03060003', '03060004', '03063002', '04010001', '04010002', '04010004', '04020001', '04020002', '04020003', '04020004', '04020005', '05010001', '05010002', '05010003', '05010004', '06010001', '06010002', '07010001', '07010002', '07010003', '07010004', '07010005', '07010006', '07010008', '07010011', '07010012', '07010013', '07010014', '07010024', '07010032', '07020001', '07020002', '07020003', '07020004', '07030001', '07030002', '07040001', '07040002', '07040003', '07040005', '07040006'], help='xml files dir')
    args = parser.parse_args()

    xml_path = args.xml_path
    txt_path = args.txt_path
    classes = args.classes

    convert_annotation(class_list=classes, xml_path=xml_path, save_path=txt_path)
