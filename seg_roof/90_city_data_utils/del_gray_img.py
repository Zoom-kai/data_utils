import os
import cv2
import shutil
from tqdm import tqdm
import matplotlib.pyplot as plt


img_path = "/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/dataset/images_png"
mask_path = "/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/dataset/masks_png"

mv_path_img = "/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/dataset/images_png_del"
mv_path_mask = "/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/dataset/masks_png_del"

if not os.path.exists(mv_path_img):
    os.makedirs(mv_path_img)

if not os.path.exists(mv_path_mask):
    os.makedirs(mv_path_mask)

img_list = os.listdir(img_path)
for name in tqdm(img_list):

    img = cv2.imread(os.path.join(img_path, name))
    img_0 = img[:, :, 0]
    img_panduan = img_0[img_0 == 192]
    # print(img_0,  11111111111111111)
    # print(img_panduan)
    print(len(img_panduan.tolist()))
    if len(img_panduan.tolist()) > 30000:

        shutil.move(os.path.join(img_path, name), mv_path_img)
        shutil.move(os.path.join(mask_path, name), mv_path_mask)