# -*- coding: utf-8 -*-
import os
import sys, getopt
from pycocotools.coco import COCO, maskUtils
import cv2
import numpy as np


def mkdir_os(path):
    if not os.path.exists(path):
        os.makedirs(path)


def main(argv):
    # json_file = './data/coco/annotations/instances_val2017.json'
    # dataset_dir = './data/coco/val2017/'
    # save_dir = './data/coco/vis/'

    inputfile = '/mnt/data1/zc_data/map_data/tianditu_merge/jiaoyan_map/'
    jsonfile = '/mnt/data1/zc_data/map_data/tianditu_merge/train_jiaoyan.json'
    outputfile = '/mnt/data1/zc_data/map_data/tianditu_merge/train_instance_seg'

    try:
        opts, args = getopt.getopt(argv, "hi:j:o:", ["ifile=", "jfile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -j <jsonfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -j <jsonfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-j", "--jfile"):
            jsonfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print('\n输入的文件为：', inputfile)
    print('\n输入的json为：', jsonfile)
    print('\n输出的文件为：', outputfile)

    mkdir_os(outputfile)

    coco = COCO(jsonfile)
    catIds = coco.getCatIds(catNms=['wires'])  # catIds=1 表示人这一类
    imgIds = coco.getImgIds(catIds=catIds)  # 图片id，许多值
    for i in range(len(imgIds)):
        if i % 100 == 0:
            print(i, "/", len(imgIds))
        img = coco.loadImgs(imgIds[i])[0]

        cvImage = cv2.imread(os.path.join(inputfile, img['file_name']), -1)
        cvImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
        cvImage = cv2.cvtColor(cvImage, cv2.COLOR_GRAY2BGR)

        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
        anns = coco.loadAnns(annIds)

        polygons = []
        color = []
        for ann in anns:
            if 'segmentation' in ann:
                if type(ann['segmentation']) == list:
                    # polygon
                    for seg in ann['segmentation']:
                        poly = np.array(seg).reshape((int(len(seg) / 2), 2))
                        poly_list = poly.tolist()
                        polygons.append(poly_list)
                        if ann['iscrowd'] == 0:
                            color.append([0, 0, 255])
                        if ann['iscrowd'] == 1:
                            color.append([0, 255, 255])
                else:
                    exit()
                    print("-------------")
                    # mask
                    t = imgIds[ann['image_id']]
                    if type(ann['segmentation']['counts']) == list:
                        rle = maskUtils.frPyObjects([ann['segmentation']], t['height'], t['width'])
                    else:
                        rle = [ann['segmentation']]
                    m = maskUtils.decode(rle)

                    if ann['iscrowd'] == 0:
                        color_mask = np.array([0, 0, 255])
                    if ann['iscrowd'] == 1:
                        color_mask = np.array([0, 255, 255])

                    mask = m.astype(np.bool)
                    cvImage[mask] = cvImage[mask] * 0.7 + color_mask * 0.3

        point_size = 2
        thickness = 2
        for key in range(len(polygons)):
            ndata = polygons[key]
            cur_color = color[key]
            for k in range(len(ndata)):
                data = ndata[k]
                cv2.circle(cvImage, (data[0], data[1]), point_size, (cur_color[0], cur_color[1], cur_color[2]),
                           thickness)
        cv2.imwrite(os.path.join(outputfile, img['file_name']), cvImage)


if __name__ == "__main__":
    main(sys.argv[1:])