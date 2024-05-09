import  os
import shutil
from tqdm import tqdm

img_path = "/mnt/data1/zc_data/fire_flash_yolo/fire/fire_0628/images/train"
label_path = "/mnt/data1/zc_data/fire_flash_yolo/fire/fire_0628/labels/train"


new_img_path = "/mnt/data3/zc_data/jx_0217/original/no_obj/"

if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)

img_list = os.listdir(label_path)
for img_name in tqdm(img_list):
    txt = "{}/{}".format(label_path, img_name)
    img = img_name.replace("images", "labels").replace("txt", "jpg")

    if not os.path.exists(os.path.join(img_path, img)):
        shutil.move(txt, new_img_path)
