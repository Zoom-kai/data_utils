import  os
import shutil
from tqdm import tqdm
from shutil import copy2


# cp img labels

# img_path = "/mnt/data3/zc_data/jx_0217/original/data/loujian/loujian_che"
#
# label_path = "/mnt/data3/zc_data/che/test/labels/"
# new_img_path = "/mnt/data3/zc_data/jx_0217/original/data/loujian/loujian_che_labels"

# img_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/person/images/val/"
#
# label_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/person_yolo/"
#
# new_label_path = "/mnt/data1/zc_data/dianchang/dianchang_0308/person/labels/val/"

img_path = "/mnt/data1/zc_data/dianchang/dianchang_06/jinglianwen_0621/images/"

label_path = "/mnt/data1/zc_data/dianchang/dianchang_06/jinglianwen_0621/yolo_labels_fzq"

new_label_path = "/mnt/data1/zc_data/dianchang/dianchang_5yue/safebelt/wuyong"

new_img_path = "/mnt/data1/zc_data/dianchang/dianchang_06/jinglianwen_0621/images_fzq"


if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)

if not os.path.exists(new_label_path):
    os.makedirs(new_label_path)

img_list = os.listdir(img_path)
for img_name in tqdm(img_list):

    img = os.path.join(img_path, img_name)
    txt = os.path.join(label_path, img_name.replace(img_name.split('.')[-1], "txt"))

    print(os.path.exists(txt))
    if os.path.exists(txt):

        # shutil.move(img, new_img_path)
        # shutil.move(txt, new_label_path)

        copy2(img, new_img_path)

