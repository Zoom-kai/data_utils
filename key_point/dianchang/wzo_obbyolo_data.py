import shapely
import shapely.geometry
import json
import numpy as np
import os
import glob
import cv2
import shutil
from random import shuffle
from utils.general import xywhrm2xyxyxyxy, xyxyxyxy2xywhrm, xyxyxyxyn2xyxyxyxy

oneD2twoD = lambda x: [(x[2 * i], x[2 * i + 1]) for i in
                       range(len(x) // 2)]  # one D [x, y, x, y, x, y, ...] to [(x, y), (x, y), ...]


def normalize_anchors(label, img_h, img_w):
    """
        rotate
        FROM class id, x, y, w, h, re, im (unnormalized)
        TO class id (unchanged), x, y, w, h, re, im (normalized to [0, 1])
    """
    label = np.array(label)
    label_pixel = np.zeros((9,))
    label_pixel[0] = label[0]
    label_pixel[1:] = xywhrm2xyxyxyxy(np.array([label[1:]]))[0]
    label[[1, 3]] = label[[1, 3]] / img_w
    label[[2, 4]] = label[[2, 4]] / img_h
    #     label[1::2] = label[1::2].clip(0., img_w)/img_w
    #     label[2::2] = label[2::2].clip(0., img_h)/img_h
    return label, label_pixel


def unnormalize_anchors(label, img_h, img_w):
    """
        From class id ,x, y, x, y, x, y, x, y(unnormalized)
        To class id, x, y, x, y, x, y, x, y(normalized to [0,1])
    """
    label = np.array(label)

    label[0::2] = label[0::2] * img_w
    label[1::2] = label[1::2] * img_h
    #     label[1::2] = label[1::2].clip(0., img_w)/img_w
    #     label[2::2] = label[2::2].clip(0., img_h)/img_h
    return label


def main():
    f = open("wrong2.txt", 'w')
    classes_list = ["脚手架", "脚手架平台板", "脚手架横杆"]
    json_path = "/mnt/date1/wzo_data/dianchang_zong_shuju/json_labels/IMG20230208152044.jpg.json"
    img_dir = "/mnt/date1/wzo_data/dianchang_zong_shuju/images/train/"
    data = json.load(open(json_path, 'r'))
    img_path = os.path.join(img_dir, data["imagePath"])
    img = cv2.imread(img_path)
    img_2 = img.copy()
    for ob in data['shapes']:
        shape_type = ob['shape_type']
        if shape_type == "polygon":
            segment = ob['points']
            segment = np.array(segment, dtype=np.int32)
            segment = segment.flatten().tolist()
            segment = oneD2twoD(segment + segment[:2])
            multipoint = shapely.geometry.MultiPoint(segment)
            try:
                label = [classes_list.index(ob["label"]), *list(
                    xyxyxyxy2xywhrm(np.array(multipoint.minimum_rotated_rectangle.exterior.coords[:-1]).ravel())[0])]
            except:
                label = [int(ob["label"]), *list(
                    xyxyxyxy2xywhrm(np.array(multipoint.minimum_rotated_rectangle.exterior.coords[:-1]).ravel())[0])]
                f.write()
            label, label_pixel = normalize_anchors(label, data['imageHeight'], data['imageWidth'])
            rect = label_pixel[1:].reshape(-1, 2).astype(np.int32)
            cv2.polylines(img, [rect], True, (0, 0, 255), 2)
            label_2 = np.zeros(9)
            label_2[0] = label[0]
            label[1:5] = unnormalize_anchors(label[1:5], data['imageHeight'], data['imageWidth'])
            label_2[1:] = xywhrm2xyxyxyxy(label[1:].reshape(-1, 6))
            # label_2[1:] = xyxyxyxyn2xyxyxyxy(label_2[1:].reshape(-1,8),data['imageWidth'],data['imageHeight'])
            rect = label_2[1:].reshape(-1, 2).astype(np.int32)
            cv2.polylines(img_2, [rect], True, (0, 0, 255), 2)
        elif shape_type == "rectangle":
            segment = ob['points']
            segment.insert(1, [segment[1][0], segment[0][1]])
            segment.append([segment[0][0], segment[2][1]])
            segment = np.array(segment, dtype=np.int32)
            segment = segment.flatten().tolist()
            segment = oneD2twoD(segment + segment[:2])
            multipoint = shapely.geometry.MultiPoint(segment)
            try:
                label = [classes_list.index(ob["label"]), *list(
                    xyxyxyxy2xywhrm(np.array(multipoint.minimum_rotated_rectangle.exterior.coords[:-1]).ravel())[0])]
            except:
                label = [int(ob["label"]), *list(
                    xyxyxyxy2xywhrm(np.array(multipoint.minimum_rotated_rectangle.exterior.coords[:-1]).ravel())[0])]
            label, label_pixel = normalize_anchors(label, data['imageHeight'], data['imageWidth'])
            rect = label_pixel[1:].reshape(-1, 2).astype(np.int32)
            cv2.polylines(img, [rect], True, (0, 0, 255), 2)
            label_2 = np.zeros(9)
            label_2[0] = label[0]
            label[1:5] = unnormalize_anchors(label[1:5], data['imageHeight'], data['imageWidth'])
            label_2[1:] = xywhrm2xyxyxyxy(label[1:].reshape(-1, 6))
            # label_2[1:] = xyxyxyxyn2xyxyxyxy(label_2[1:].reshape(-1,8),data['imageWidth'],data['imageHeight'])
            rect = label_2[1:].reshape(-1, 2).astype(np.int32)
            cv2.polylines(img_2, [rect], True, (0, 0, 255), 2)
    cv2.imwrite("pol.png", img)
    cv2.imwrite("pol2.png", img_2)


def main2():
    classes_list = ["脚手架", "脚手架平台板", "脚手架横杆"]
    json_path = "/mnt/date1/wzo_data/dianchang_zong_shuju/json_labels/IMG_20230209_110400.jpg.json"
    img_dir = "/mnt/date1/wzo_data/dianchang_zong_shuju/images/train/"
    data = json.load(open(json_path, 'r'))
    img_path = os.path.join(img_dir, data["imagePath"])
    img = cv2.imread(img_path)
    for ob in data['shapes']:
        shape_type = ob['shape_type']
        if shape_type == "polygon":
            segment = ob['points']
            segment_a = np.array(segment, dtype=np.int32)
            rect = cv2.minAreaRect(segment_a)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
    cv2.imwrite("pol1.png", img)


def json_2_rotate_txt(json_path, save_dir, img_root, img_des_dir, classes_list):
    # classes_list = ["脚手架","脚手架平台板","脚手架横杆"]
    data = json.load(open(json_path, 'r'))
    save_name = os.path.join(save_dir, os.path.basename(json_path).split('.')[0] + '.txt')
    f_txt = open(save_name, 'w')
    for ob in data['shapes']:
        shape_type = ob['shape_type']
        if shape_type == "polygon":
            segment = ob['points']
            if len(segment) > 2:
                segment = np.array(segment, dtype=np.int32)
                segment = segment.flatten().tolist()

                segment = oneD2twoD(segment + segment[:2])
                multipoint = shapely.geometry.MultiPoint(segment)
                # try:
                label = np.array(multipoint.minimum_rotated_rectangle.exterior.coords[:-1]).ravel().tolist()
                # except:
                # print(json_path,ob['points'])
                # label, _ = normalize_anchors(label, data['imageHeight'], data['imageWidth'])
                f_txt.write(
                    " ".join([str(a) for a in label]) + ' ' + str(classes_list.index(ob["label"])) + ' ' + "0" + '\n')
            else:
                continue
        elif shape_type == "rectangle":
            segment = ob['points']
            segment.insert(1, [segment[1][0], segment[0][1]])
            segment.append([segment[0][0], segment[2][1]])
            segment = np.array(segment, dtype=np.int32)
            segment = segment.flatten().tolist()
            segment = oneD2twoD(segment + segment[:2])
            multipoint = shapely.geometry.MultiPoint(segment)
            try:
                label = np.array(multipoint.minimum_rotated_rectangle.exterior.coords[:-1]).ravel().tolist()
            except:
                label = np.array(multipoint.minimum_rotated_rectangle.exterior.coords[:-1]).ravel().tolist()
            # label, _ = normalize_anchors(label, data['imageHeight'], data['imageWidth'])
            f_txt.write(
                " ".join([str(a) for a in label]) + ' ' + str(classes_list.index(ob["label"])) + ' ' + "0" + '\n')
    f_txt.close()
    img_src = os.path.join(img_root, os.path.basename(data['imagePath']))
    shutil.copy(img_src, img_des_dir)
    return os.path.join(img_des_dir, os.path.basename(data['imagePath']))


def main_(des_dir_label, root_dir_json, img_root, img_des_dir, classes_list):
    if not os.path.exists(des_dir_label):
        os.makedirs(des_dir_label)
    source_jsons = sorted(glob.glob(root_dir_json + '/*.json'))
    shuffle(source_jsons)

    train_txt = os.path.join(des_dir_label, 'imagefilename.txt')

    with open(train_txt, 'w') as f:
        for s_json in source_jsons:
            # try:
            des_img = json_2_rotate_txt(s_json, des_dir_label, img_root, img_des_dir, classes_list)
            # except:
            f.write(des_img + '\n')
            # print(s_json)


if __name__ == "__main__":
    save_dir = "/mnt/date1/wzo_data/dianchang_zong_shuju/labelTxt/train/"
    root_dir_json = "/mnt/date1/wzo_data/dianchang_zong_shuju/json_labels/"
    img_root = "/mnt/date1/wzo_data/dianchang_zong_shuju/images_all/train/"
    img_des_dir = "/mnt/date1/wzo_data/dianchang_zong_shuju/images/train/"
    classes_list = ["脚手架", "脚手架平台板", "脚手架横杆"]
    main_(save_dir, root_dir_json, img_root, img_des_dir, classes_list)
    # main()