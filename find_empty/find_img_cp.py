import  os
import shutil
from tqdm import tqdm
from shutil import copy2


img_path = "/mnt/data1/zc_data/smoke_data/smoke_yolo_merge_0701/jx_data/smk_jx_0504/images/val"

new_img_path = "/mnt/data3/zc_data/jx_0217/original/data/images"

new_path = "/mnt/data1/zc_data/smoke_data/smoke_yolo_merge_0701/fuyangben_jx_ori"

if not os.path.exists(new_path):
    os.makedirs(new_path)

img_list = os.listdir(img_path)
for img_name in tqdm(img_list):

    img = os.path.join(img_path, img_name)

    new_img = os.path.join(new_img_path, img_name)

    if os.path.exists(new_img):
        copy2(new_img, new_path)
