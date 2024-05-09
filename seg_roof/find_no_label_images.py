import  os
import shutil
from tqdm import tqdm

img_path = "/mnt/data1/zc_data/map_data/tianditu_merge/images/val"
# label_path = "/mnt/data3/zc_data/cls_16_data/resize/labels/"
new_img_path = img_path+"_no_label/"


if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)


img_list = os.listdir(img_path)
num = 0
for img_name in tqdm(img_list):
    img = "{}/{}".format(img_path, img_name)
    txt = img.replace("images", "masks")

    if not os.path.exists(txt):
        shutil.move(img, new_img_path)
        num+= 1

print("no labels img:", num)