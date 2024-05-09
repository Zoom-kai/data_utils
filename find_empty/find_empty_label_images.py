import  os
import shutil
from tqdm import tqdm
from shutil import copy2

img_path = r"/mnt/data1/zc_data/dianchang/dianchang_5yue/dianchang_all_0613_img_ori_7049_1280"
label_path = r"/mnt/data1/zc_data/dianchang/dianchang_5yue/miehuoqi/labels"

# empty_img_path = img_path + "empty"
# empty_label_path = label_path + "empty"

empty_img_path = r"/mnt/data1/zc_data/smoke_data/classify_dataset/smoke_fuyangben"
empty_label_path = r"/mnt/data1/zc_data/dianchang/dianchang_5yue/gongzhuang/labels/hattrain_emp"

if not os.path.exists(empty_img_path):
    os.makedirs(empty_img_path)
if not os.path.exists(empty_label_path):
    os.makedirs(empty_label_path)

img_list = os.listdir(img_path)
a = 0
for img_name in tqdm(img_list):
    img = "{}/{}".format(img_path, img_name)
    houzui = img.split('.')[-1]
    txt = "{}/{}".format(label_path, img_name.replace(houzui, "txt"))

    # print(txt)
    # print(os.path.getsize(txt))
    if not os.path.exists(txt):
        shutil.move(img, empty_img_path)
        continue

    if not os.path.getsize(txt):
        a += 1
        print(a)

        # shutil.move(img, empty_img_path)
        shutil.move(txt, empty_label_path)

    # if os.path.getsize(txt):
    #     a += 1
    #     print(a)
    #     copy2(txt, empty_label_path)
    #     copy2(img, empty_img_path)