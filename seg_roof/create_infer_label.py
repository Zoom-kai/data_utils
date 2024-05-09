import os
import json
import random
import numpy as np

cls_list = ['Concrete', 'Steel_Structure', 'Rusted_steel_structure', 'Have_Accessory_roof', 'Tile_roof', 'Other_roofs', 'Installed_photovoltaic ', '111']

img_pash = r"/mnt/data1/zc_code/tmp/pycharm_project_455/test_images/patch_img"

train_label = r'E:\datasets\gudewei\labels\train_ann.txt'
val_label = r'/mnt/data1/zc_code/tmp/pycharm_project_455/test_images/infer_ann.txt'
# num = len(js_list) * 0.9
n = 0

# t = open(train_label, 'w')
v = open(val_label, 'w')
img_list = os.listdir(img_pash)

for js_name in img_list:

    name = js_name
    cls = 5
    # n += 1
    # if n < num:
    # t.write("{} {} \n".format(name, cls))
    # elif n >= num:
    v.write("{} {} \n".format(name, cls))

# t.close()
v.close()
