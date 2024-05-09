import argparse
import cv2
import json
import os
from tqdm import tqdm

# -*- coding=utf-8 -*-



def yolo2coco(image_dir, label_dir, classes, save, image_txt=None):
    PRE_DEFINE_CATEGORIES = {}
    imgs = os.listdir(image_dir)
    lbls = [_.rsplit('.')[0] + '.txt' for _ in imgs]

    images = []
    annotations = []

    categories = PRE_DEFINE_CATEGORIES

    json_dict = {
        "type": "instances",
        "categories": [],
        "images": [],
        "annotations": []
    }


    for i,img in enumerate(tqdm(imgs)):
        #if img：
        lbl = img.replace("{}".format(img.split(".")[-1]), "txt")
        image_array = cv2.imread(os.path.join(image_dir, img))
        if image_array is None:
            print("CANT open {}".format(os.path.join(image_dir, img)))
            continue
        ih, iw, _ = image_array.shape
        # image_id = len(images)
        if not os.path.exists(os.path.join(label_dir, lbl)):
            continue

        image = {
            'file_name': img,
            'height': ih,
            'width': iw,
            'id': i
        }
        json_dict['images'].append(image)

        with open(os.path.join(label_dir, lbl)) as f:
            for line in f.readlines():
                line = line.strip().split(' ')
                category_id = int(line[0])
                if category_id > 90 :
                    continue
                print(category_id)
                category = classes[category_id]
                if category not in categories:
                    new_id = len(categories)
                    categories[category] = new_id

                x, y, w, h = [float(_) for _ in line[1:5]]
                x, y, w, h = x * iw, y * ih, w * iw, h * ih

                annotation = dict()
                annotation['id'] = len(annotations)
                annotation['category_id'] = category_id
                annotation['image_id'] = i
                annotation['area'] = w * h
                annotation['bbox'] = [x - w / 2, y - h / 2, w, h]
                annotation['iscrowd'] = 0
                annotation['ignore'] = 0

                json_dict['annotations'].append(annotation)
                #print(annotations)

        # 写入类别ID字典
        for cate, cid in categories.items():
            cat = {'supercategory': 'none', 'id': cid, 'name': cate}
            json_dict['categories'].append(cat)
        # 导出到json
        with open(save, 'w') as json_fp:
            json_str = json.dumps(json_dict, indent=4)
            json_fp.write(json_str)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', type=str, default=r"/mnt/data1/zc_data/green_net_all/green_net_600/images/val")              # img 路径
    parser.add_argument('--labels', type=str, default="/mnt/data1/zc_data/green_net_all/green_net_600/labels/val")           # txt 标签路径
    parser.add_argument('--classes', type=list, default=
    # ["YX001", 'TG001']
      ["green-net"]
    # ['02010001', '02013001', '02010002', '02010006', '02010004', '02010005', '02020001', '02020003', '02020004',
    #  '02030001', '02030002', '03010001', '03010002', '03011002', '03010003', '03013001', '03020001', '03020003',
    #  '03021002', '03030001', '03030002', '03030003', '03030004', '03030006', '03030005', '03030007', '03040001',
    #  '03040002', '03040003', '03040005', '03040007', '03040008', '03040009', '03040010', '03040011', '03040012',
    #  '03040013', '03040014', '03040015', '03040016', '03040017', '03040018', '03040023', '03040024', '03040025',
    #  '03050002', '03051001', '03052001', '03060001', '03060002', '03060003', '03060004', '03063002', '04010001',
    #  '04010002', '04010004', '04020001', '04020002', '04020003', '04020004', '04020005', '05010001', '05010002',
    #  '05010003', '05010004', '06010001', '06010002', '07010001', '07010002', '07010003', '07010004', '07010005',
    #  '07010006', '07010008', '07010011', '07010012', '07010013', '07010014', '07010024', '07010032', '07020001',
    #  '07020002', '07020003', '07020004', '07030001', '07030002', '07040001', '07040002', '07040003', '07040005',
    #  '07040006']
                        )

    # 类别
    parser.add_argument('--save', type=str, default="/mnt/data1/zc_data/green_net_all/green_net_600/val.json")       # coco标签文件保存路径

    args = parser.parse_args()
    yolo2coco(args.images, args.labels, args.classes, args.save)