import  os
import shutil
from tqdm import tqdm
from shutil import copy2

# 空lab 对应的图片不删除 ？

label_path = "/mnt/data1/zc_data/dianchang/dianchang_7yue_dk/data_jlw/aqd_pose_labels/"

empty_label_path = "/mnt/data1/zc_data/dianchang/dianchang_06/haitian_0621/empty_pose_del"

if not os.path.exists(empty_label_path):
    os.makedirs(empty_label_path)

label_list = os.listdir(label_path)
a = 0
for txt_name in tqdm(label_list):
    txt = "{}/{}".format(label_path, txt_name)

    # 把空的txt移走
    if not os.path.getsize(txt):
        a += 1
        print(a)
        shutil.move(txt, empty_label_path)

    # 把非空的txt移走
    # if os.path.getsize(txt):
    #     a += 1
    #     print(a)
    #     copy2(txt, empty_label_path)
    #     copy2(img, empty_img_path)