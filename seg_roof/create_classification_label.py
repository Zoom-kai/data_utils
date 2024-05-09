import os
import json
import random
import numpy as np

cls_list = ['Concrete', 'Steel_Structure', 'Rusted_steel_structure', 'Have_Accessory_roof', 'Tile_roof', 'Other_roofs', 'Installed_photovoltaic ', '111']

js_pash = r"E:\datasets\gudewei\infer_input_json"
js_list = os.listdir(js_pash)
np.random.shuffle(js_list)

train_label = r'E:\datasets\gudewei\labels\train_ann.txt'
val_label = r'E:\datasets\gudewei\labels\infer_ann.txt'
# num = len(js_list) * 0.9
n = 0

# t = open(train_label, 'w')
v = open(val_label, 'w')


for js_name in js_list:
    file = open("{}/{}".format(js_pash, js_name), encoding="utf-8")
    js_file = json.loads(file.readline())
    print(js_file)
    out = js_file["outputs"]
    obj = out['object'][0]
    cls = obj['name']
    cls = cls_list.index(cls)

    name = js_name.split(".")[0]+'.png'


    # n += 1
    # if n < num:
    # t.write("{} {} \n".format(name, cls))
    # elif n >= num:
    v.write("{} {} \n".format(name, cls))

# t.close()
v.close()
