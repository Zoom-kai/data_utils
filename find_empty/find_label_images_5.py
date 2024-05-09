import  os
import shutil
from tqdm import tqdm
from shutil import copy2


# 根据labels 从images里面找出有对应文件名的图片，并把图片移动到 new_img_path

# cp img labels

# img_path = "/mnt/data3/zc_data/jx_0217/original/data/loujian/loujian_che"
#
# label_path = "/mnt/data3/zc_data/che/test/labels/"
# new_img_path = "/mnt/data3/zc_data/jx_0217/original/data/loujian/loujian_che_labels"

img_path = "/mnt/data1/zc_data/dianchang/dianchang_5yue/dianchang_all_0613_img_ori_7049_1280"

label_path = "/mnt/data1/zc_data/dianchang/dianchang_5yue/miehuoqi/labels"

new_img_path = "/mnt/data1/zc_data/dianchang/dianchang_5yue/miehuoqi/images"

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

    print(os.path.exists(txt))
    if os.path.exists(txt):
        shutil.move(img, new_img_path)
        # copy2(img, new_img_path)

