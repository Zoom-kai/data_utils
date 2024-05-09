import json
import os
import cv2


img_path = r"E:\datasets\gudewei\infer_input"
img_list = os.listdir(img_path)
json_save_path = r"E:\datasets\gudewei\infer_input_json"

if not os.path.exists(json_save_path):
    os.makedirs(json_save_path)

cls_list = ['Concrete', 'Steel_Structure', 'Rusted_steel_structure', '111', 'Tile_roof']

for img_name in img_list:
    img = cv2.imread("{}/{}".format(img_path, img_name))
    cls = cls_list[int(img_name[0])]

    print(212422424334, cls)
    dic_name = {}
    dic_name['name'] = cls
    dic_object = {}
    dic_object['object'] = [dic_name]
    dic_output = {}
    dic_output['outputs'] = dic_object
    print(dic_output)
    json_name = img_name.split(".")[0]+".json"
    json_dict = open(os.path.join(json_save_path, json_name), 'w')

    json.dump(dic_output, json_dict)