import os
from tqdm import tqdm
from shutil import copy
from random import shuffle
import json

all_cats = [0]
# all_cats = [56, 60, 61, 62, 68, 81, 89]
# all_cats = [12, 20, 29, 58, 56, 60, 61, 62]
# all_cats = [12, 20]

with open('/mnt/data1/zc_data/cls_16_data/train_all_info.json') as f:
    d = json.load(f)['cat2imgs']
    d = {int(k): v for k, v in d.items()}
for cat in tqdm(all_cats):
    os.makedirs('/mnt/data3/zc_data/cls_16_data/images/train_{:d}/'.format(cat), exist_ok=True)
    os.makedirs('/mnt/data3/zc_data/cls_16_data/images/val_{:d}/'.format(cat), exist_ok=True)
    os.makedirs('/mnt/data3/zc_data/cls_16_data/labels/train_{:d}/'.format(cat), exist_ok=True)
    os.makedirs('/mnt/data3/zc_data/cls_16_data/labels/val_{:d}/'.format(cat), exist_ok=True)
    v = d[cat]

    shuffle(v)
    train = v[:int(len(v)*0.8+0.5)]
    test = v[int(len(v)*0.8+0.5):]
    print(cat)
    # if not cat == 56:
        # print(cat==56)
    for _ in tqdm(train):
        if not os.path.exists('/mnt/data1/zc_data/da_model_merge/images/'+_[:-3]+'jpg'):
            continue
        if not os.path.exists(os.path.join('/mnt/data1/zc_data/da_model_merge/yolo_labels/', _)):
            continue
        # print(os.path.join('/mnt/data1/zc_data/da_model_merge/yolo_labels/', _))

        copy('/mnt/data1/zc_data/da_model_merge/images/'+_[:-3]+'jpg', '/mnt/data3/zc_data/cls_16_data/images/train_{:d}/'.format(cat))
        with open(os.path.join('/mnt/data1/zc_data/da_model_merge/yolo_labels/', _)) as f:
            lines = [_ for _ in f.readlines() if _.startswith('{:d} '.format(cat))]
            # print(lines)
            f.close()
        with open(os.path.join('/mnt/data3/zc_data/cls_16_data/labels/train_{:d}/'.format(cat), _), 'w') as f:
            for line in lines:

                # print("line[0] == cat, {}, {}".format(line[0], cat))
                line1 = "0" + line[2:]
                # print(line1)
                f.write(line1)

            f.close()
    for _ in tqdm(test):
        if not os.path.exists('/mnt/data1/zc_data/da_model_merge/images/'+_[:-3]+'jpg'):
            continue
        if not os.path.exists(os.path.join('/mnt/data1/zc_data/da_model_merge/yolo_labels/', _)):
            continue
        #copy('/mnt/data1/zc_data/da_model_merge/images/'+_[:-3]+'jpg', '/mnt/data3/zc_data/cls_16_data/images/val_{:d}/'.format(cat))
        with open(os.path.join('/mnt/data1/zc_data/da_model_merge/yolo_labels', _)) as f:
            lines = [_ for _ in f.readlines() if _.startswith('{:d} '.format(cat))]
            f.close()
        with open(os.path.join('/mnt/data3/zc_data/cls_16_data/labels/val_{:d}/'.format(cat), _), 'w') as f:
            for line in lines:
                # print(line[0] == "{}".format(cat), line[0], cat)
                # print("line[0] == cat, {}, {}".format(line[0], cat))
                line1 = "0" + line[2:]
                # print(line1)
                f.write(line1)
            f.close()
# image_dir = "images/train_47818"
# label_dir = "labels/train_47818"
# sub_image_dir = "images/train_1097"
# sub_label_dir = "labels/train_1097"
# os.makedirs(sub_image_dir, exist_ok=True)
# os.makedirs(sub_label_dir, exist_ok=True)
# for image_file in tqdm(os.listdir(image_dir)):
#     label_file = image_file.rsplit('.', 1)[0] + '.txt'
#     if not os.path.exists(os.path.join(label_dir, label_file)):
#         continue

#     labels = []
#     with open(os.path.join(label_dir, label_file)) as f:
#         for line in f.readlines():
#             line = line.split(' ')
#             # if line[0] == '5':
#             if line[0] == '35':
#                 line[0] = '0'
#                 labels.append(' '.join(line))
#             # if line[0] == '18':
#             if line[0] == '55':
#                 line[0] = '1'
#                 labels.append(' '.join(line))
#     if len(labels) == 0:
#         continue
#     copy(os.path.join(image_dir, image_file), sub_image_dir)
#     with open(os.path.join(sub_label_dir, label_file), 'w') as f:
#         for line in labels:
#             f.write(line)

