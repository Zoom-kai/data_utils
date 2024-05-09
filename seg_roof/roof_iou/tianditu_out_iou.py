import os
import cv2
import matplotlib.pyplot as plt
# 直接两张图计算IOU

tianditu_mask_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data/train/jiedaotu_patch/"
out_mask_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data/output_old_model_pitch/"
new_mask_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/jiaoyan_mask"
img_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data/train/img"

new_img_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/statistics_tianditu_1"
preview_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/jiaoyan_map_iou_images_add"

iou_thres = 0.75

if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)

if not os.path.exists(new_mask_path):
    os.makedirs(new_mask_path)

if not os.path.exists(preview_path):
    os.makedirs(preview_path)

# tianditu_mask_list = os.listdir(tianditu_mask_path)
img_list = os.listdir(img_path)
for name in img_list:
    print(name)
    tianditu_mask = cv2.imread(os.path.join(tianditu_mask_path, name), cv2.IMREAD_GRAYSCALE)
    out_mask = cv2.imread(os.path.join(out_mask_path, name), cv2.IMREAD_GRAYSCALE)

    # out_mask[out_mask != 255] = 0
    # print(out_mask[out_mask!=0], tianditu_mask[tianditu_mask!=0])
    # exit()
    out_mask[out_mask != 0] = 1
    tianditu_mask[tianditu_mask != 0] = 1

    # print(out_mask)
    Intersecting_graph = tianditu_mask

    # Intersecting_graph[Intersecting_graph & out_mask] = 0
    # Intersecting_graph[Intersecting_graph == out_mask] = 1
    Intersecting_graph = Intersecting_graph & out_mask
    # print(Intersecting_graph, Intersecting_graph.shape)

    # print(Intersecting_graph.sum(), tianditu_mask.sum(), out_mask.sum())
    iou = Intersecting_graph.sum()/min(tianditu_mask.sum(), out_mask.sum())
    # print(iou)


    # img = cv2.imread(os.path.join(img_path, name))
    # img[tianditu_mask == 1, 0] = 255
    # iou = "{}".format(iou)
    # font = cv2.FONT_HERSHEY_COMPLEX
    # color = (255, 0, 100)
    # cv2.putText(img, iou, (50, 50), font, 3, color, 3)
    # cv2.imwrite("{}/{}".format(preview_path, name), img)


    # if iou> iou_thres:
    if iou < 0.3:
        img = cv2.imread(os.path.join(img_path, name))
        # duoyude = out_mask - tianditu_mask
        img0 = img.copy()
        img[tianditu_mask == 1, 0] = 255
        img0[out_mask==1, 0] = 255
        name = name.split(".")[0]
        iou = round(iou, 2)
        cv2.imwrite("{}/{}_out_{}.png".format(new_img_path, name, iou), img0)
        cv2.imwrite("{}/{}_tianditu_{}.png".format(new_img_path, name, iou), img)



        # duoyude[duoyude != 1] = 0


## test
# import numpy as np
# import torch
# p1 = np.arange(2, 5)
# p2 = np.arange(2, 5)
# print(p1, p2)
# print(p1==p2)
# print(sum(p1))
# print(p1&p2/min(sum(p1), sum(p2)))

