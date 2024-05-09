import  os
import shutil
from tqdm import tqdm
from shutil import copy2
import cv2

# cp img labels

# img_path = "/mnt/data3/zc_data/jx_0217/original/data/loujian/loujian_che"
#
# label_path = "/mnt/data3/zc_data/che/test/labels/"
# new_img_path = "/mnt/data3/zc_data/jx_0217/original/data/loujian/loujian_che_labels"

img_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/images"

label_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/aqd_pose/labels/"
new_img_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/aqd_pose/images/"




if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)

img_list = os.listdir(img_path)
new_shape = (1280, 1280)
for img_name in tqdm(img_list):
    # print(img_name)
    # if img_name.split('.')[-1] != 'jpeg':
    #     continue
    # print(img_name)
    img_p = os.path.join(img_path, img_name)
    txt = os.path.join(label_path, img_name.replace(img_name.split('.')[-1], "txt"))
    print(img_p)
    if os.path.exists(txt):
        img = cv2.imread("{}".format(img_p))
        shape = img.shape[:2]
        # print(shape)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = int(round(shape[0] * r)), int(round(shape[1] * r))
        # print(shape)
        # print(new_unpad)
        # exit()
        new_img = cv2.resize(img, (new_unpad[1], new_unpad[0]))
        cv2.imwrite("{}/{}".format(new_img_path, img_name), new_img)

