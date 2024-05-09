import  os
import shutil
from tqdm import tqdm
from shutil import copy2

img_path = "/mnt/data3/zc_data/che/images/train"
label_path = "/mnt/data3/zc_data/che/test/labels_yolo"
#  /mnt/data3/zc_data/che/test/images/val

# new_img_path = "/mnt/data3/zc_data/che/negative_sample/fake_label"
# new_path = "/mnt/data3/zc_data/che/negative_sample/fake"
new_img_path = '/mnt/data3/zc_data/che/test/images'

if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)

img_list = os.listdir(img_path)
a = 0
for img_name in tqdm(img_list):
    # print(img_name)
    if img_name.split('.')[-1] != 'jpeg':
        continue
    # print(img_name)
    img = os.path.join(img_path, img_name)
    txt = os.path.join(label_path, img_name.replace("jpeg", "txt"))

    # neg_img = os.path.join(new_img_path, img_name.replace("jpeg", "txt"))

    if os.path.exists(txt):
        copy2(img, new_img_path)
        # copy2(txt, new_path)
        a += 1
        print(a)