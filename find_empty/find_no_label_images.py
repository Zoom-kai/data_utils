import  os
import shutil
from tqdm import tqdm
from shutil import copy2
img_path = "/mnt/data3/zc_data/che/images/train"
label_path = "/mnt/data3/zc_data/che/images/labels/train"
new_img_path = "/mnt/data3/zc_data/che/no_labels_data/"

if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)

img_list = os.listdir(img_path)
for img_name in tqdm(img_list):

    img = os.path.join(img_path, img_name)
    txt = os.path.join(label_path, img_name.replace(img_name.split('.')[-1], "txt"))

    if not os.path.exists(txt):
        shutil.move(img, new_img_path)
        # copy2(img, new_img_path)

