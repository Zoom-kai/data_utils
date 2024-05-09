import os
import cv2
import numpy as np
import shutil
from matplotlib.pyplot import plot
import tqdm

img_path = r"/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/suzhou_png"
# /mnt/data1/zc_code/rooftopsegmatation-master/output_predict/suzhou_shidian_1024_w512_mask_da_ep29/2/
mask_path = r"/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/suzhou_tianditu_mask_no_erode_quhei/"
add_save_path = r"/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/suzhou_png_add_tianditu_mask_quhei"

# img_path = r"/mnt/data1/zc_data/map_data/china_90_city_datasets/Simplified_Version_1/Tier2/Shenzhen/dataset/images"
# mask_path = r"/mnt/data1/zc_data/map_data/china_90_city_datasets/Simplified_Version_1/Tier2/Shenzhen/dataset/masks"
# add_save_path = r"/mnt/data1/zc_data/map_data/china_90_city_datasets/Simplified_Version_1/Tier2/Shenzhen/dataset/images_add"

# img_path = r"/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/jiaoyan_map"
# mask_path = r"/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/jiaoyan_mask"
# add_save_path = r"/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/images_add_jiaoyan111"
if not os.path.exists(add_save_path):
    os.makedirs(add_save_path)

print(111111111111111222222222222222222221111111111111111)

img_list = os.listdir(mask_path)
np.random.shuffle(img_list)

top, bottom, left, right = 0, 0, 0, 0
num = 0
for img_name in img_list:
    print(img_name)
    img = cv2.imread("{}/{}".format(img_path, img_name))
    h, w, c = img.shape
    mask_name = img_name
    if img_name.split(".")[-1] == "tif":
        mask_name = "npy_img_{}".format(img_name.replace("tif", "png"))
    # print(mask_name)
    # mask_name = img_name.replace("tif")
    # print(mask_name)
    if not os.path.exists("{}/{}".format(mask_path, mask_name)):
        print("path {}/{} not exist !".format(mask_path, mask_name))
        continue
    mask = cv2.imread("{}/{}".format(mask_path, mask_name), cv2.IMREAD_GRAYSCALE)
    mask = cv2.resize(mask, (w, h))

    mask[mask!= 0] = 1
    print(mask[mask!= 0])
    # mask_jud = (mask == 1).__contains__(1)
    # print(mask_jud)
    #
    # if mask_jud is False:
    #     print("not build")
    #     continue
    num += 1
    # if num > 300:
    #     break
    print(111)
    # mask_jud = (mask == 1).__contains__(1)
    print(img.shape)
    print(mask.shape)
    img[mask > 0, 0] = 255

    cv2.imwrite("{}/add_{}".format(add_save_path, img_name), img)
