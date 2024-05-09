import os
import cv2
import numpy as np
import shutil
import matplotlib.pyplot as plot
from tqdm import tqdm

img_path = r"/mnt/data1/zc_data/map_data/tianditu_merge/images/val"
mask_path = r"/mnt/data1/zc_data/map_data/tianditu_merge/mask_1_patch"
add_save_path = r"/mnt/data1/zc_data/map_data/tianditu_merge/masks/val"
if not os.path.exists(add_save_path):
    os.makedirs(add_save_path)

img_list = os.listdir(img_path)
# np.random.shuffle(img_list)
top, bottom, left, right = 0, 0, 0, 0
num = 0
for img_name in tqdm(img_list):
    # print(img_name)
    img = cv2.imread("{}/{}".format(img_path, img_name))

    mask_name = img_name
    if img_name.split(".")[-1] == "tif":
        mask_name = "npy_img_{}".format(img_name.replace("tif", "png"))
    # print(mask_name)
    # mask_name = img_name.replace("tif")
    # print(mask_name)
    if not os.path.exists("{}/{}".format(mask_path, mask_name)):
        print("path {}/{} not exist !".format(mask_path, mask_name))

    mask = cv2.imread("{}/{}".format(mask_path, mask_name), cv2.IMREAD_GRAYSCALE)

    mask_jud = (mask == 1).__contains__(1)

    if mask_jud is False:
        print("not build")
        continue

    num += 1
    # if not num % 5 == 0:
    #     continue
    # print(111)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 定义结构元素的形状和大小
    mask = cv2.morphologyEx(mask, op=cv2.MORPH_OPEN, kernel=kernel, iterations=1)
    # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 定义结构元素的形状和大小
    # mask = cv2.dilate(mask, kernel1)

    # mask1 = cv2.morphologyEx(mask, op=cv2.MORPH_CLOSE, kernel=kernel1, iterations=1)

    # mask_jud = (mask == 1).__contains__(1)
    # print(img.shape)
    # print(mask.shape)

    # img[mask1 == 1, 0] = 255
    # plot.imshow(img)
    # plot.show()

    cv2.imwrite("{}/{}".format(add_save_path, img_name), mask)

