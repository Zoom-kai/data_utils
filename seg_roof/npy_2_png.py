import cv2
import numpy as np
import  os
from tqdm import tqdm


img_path = "/mnt/data1/zc_data/map_data/train/images_png"
npy_path = "/mnt/data1/zc_data/map_data/train/images_npy"
# new_img_path = "utils/split_mask/new_img"
# img_path = "/mnt/data1/zc_data/shawdow_seg/AISD/test/images"
# npy_path = "/mnt/data1/zc_data/shawdow_seg/AISD/test/npy_images"

img_list = os.listdir(npy_path)

if not os.path.exists(img_path):
    os.makedirs(img_path)

if not os.path.exists(img_path.replace("images", "masks")):
    os.makedirs(img_path.replace("images", "masks"))

# if not os.path.exists(new_img_path):
#     os.makedirs(new_img_path)
n = 0
for img_name in tqdm(img_list):
    n += 1
    # print(img_name)

    if not n%1 == 0:
        continue
    # top, bottom, left, right = 0, 0, 0, 0
    # print(1111111111111111, img_path)
    img = np.load("{}/{}".format(npy_path, img_name))
    # img = cv2.imread("{}/{}".format(img_path, img_name), cv2.IMREAD_GRAYSCALE)
    mask = np.load("{}/{}".format(npy_path, img_name).replace("images", "masks").replace(".", "_mask."))

    mask_jud = mask.sum()
    # print(mask_jud)

    if mask_jud < 15000:
        continue

    # print(mask, mask.shape, mask[mask!=0])
    img = img[:, :, ::-1]

    cv2.imwrite("{}/{}.png".format(img_path, img_name.split(".")[0]), img)
    cv2.imwrite("{}/{}.png".format(img_path, img_name.split(".")[0]).replace("images", "masks").replace("_mask", ""), mask)
    # print("{}/{}.png".format(img_path, img_name.split(".")[0]).replace("images", "masks").replace("_mask", ""))

