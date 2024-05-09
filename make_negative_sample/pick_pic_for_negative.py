import os
from shutil import copy2
from tqdm import tqdm

wujain_path = r"/mnt/data1/zc_data/smoke_data/smoke_yolo_merge_0701/fuyangben_jiangxi_rec"
img_path = r"/mnt/data3/zc_data/jx_0217/original/data/images_1280/"

new_img_path = "/mnt/data1/zc_data/smoke_data/smoke_yolo_merge_0701/fuyangben"

num = 0
if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)
wujian_list = os.listdir(wujain_path)

for pic_name in tqdm(wujian_list):
    # if num>300 :
    #     break
    img_name = pic_name
    # a = 0
    # file = open("{}/{}".format(txt_path, txt_name), "r")
    img_o = os.path.join(img_path, img_name)

    # img_new = os.path.join(new_img_path, img_name)
    # if not os.path.exists(img_o):
    #     continue

    copy2(img_o, new_img_path)

    num +=1









