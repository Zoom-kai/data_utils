import  os
import shutil
from tqdm import tqdm
from shutil import copy2


img_path = "/mnt/data1/zc_data/dianchang/dianchang_05_data/images_ori/images"

label_path = "/mnt/data1/zc_data/dianchang/dianchang_05_data/yiran/labels"

new_img_path = "/mnt/data1/zc_data/dianchang/dianchang_05_data/yiran/images"

empty_txt = "/mnt/data1/zc_data/dianchang/dianchang_05_data/yiran/labels_empty"

if not os.path.exists(empty_txt):
    os.makedirs(empty_txt)

if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)

img_list = os.listdir(img_path)
for img_name in tqdm(img_list):
    # print(img_name)
    # if img_name.split('.')[-1] != 'jpeg':
    #     continue
    # print(img_name)
    img = os.path.join(img_path, img_name)
    txt = os.path.join(label_path, img_name.replace(img_name.split('.')[-1], "txt"))

    if os.path.exists(txt):
        if not os.path.getsize(txt):
            shutil.move(txt, empty_txt)
            continue
        # shutil.move(img, new_img_path)
        copy2(img, new_img_path)

