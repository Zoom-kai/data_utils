import cv2
import numpy as np
import  os



img_path = "/mnt/data1/zc_data/map_data/tianditu_data/img_ori"
npy_path = "/mnt/data1/zc_data/map_data/tianditu_data/img_ori_npy"
# new_img_path = "utils/split_mask/new_img"
# img_path = "/mnt/data1/zc_data/shawdow_seg/AISD/test/images"
# npy_path = "/mnt/data1/zc_data/shawdow_seg/AISD/test/npy_images"

img_list = os.listdir(img_path)

if not os.path.exists(npy_path):
    os.makedirs(npy_path)

# if not os.path.exists(new_img_path):
#     os.makedirs(new_img_path)

for img_name in img_list:
    # top, bottom, left, right = 0, 0, 0, 0
    print(1111111111111111, img_path)
    img = cv2.imread("{}/{}".format(img_path, img_name))
    # img = cv2.imread("{}/{}".format(img_path, img_name), cv2.IMREAD_GRAYSCALE)


    big_side = max(img.shape[0], img.shape[1])
    smoll_side = min(img.shape[0], img.shape[1])

    idx = list(img.shape).index(smoll_side)
    # print(idx)

    pad_h = int((512 - (img.shape[0]) % 512))
    top = int(pad_h / 2)
    bottom = pad_h - top
    pad_w = int((512 - (img.shape[1]) % 512))
    right = int(pad_w / 2)
    left = pad_w - right

    img = img[:, :, ::-1]
    np.save("{}/{}".format(npy_path, img_name.split(".")[0]), img)
