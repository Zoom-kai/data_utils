import os
import json
from tqdm import tqdm
import cv2
import random

# cp img labels

label_path = "/mnt/data3/zc_data/jx_0217/original/data/wujian/save_loujian_che_1200_5_txt"
json_path = "/mnt/data3/zc_data/jx_0217/original/data/wujian/save_loujian_che_1200_5_txt.json"
img_path = "/mnt/data3/zc_data/jx_0217/original/data/images"
output_img_path = '/mnt/data3/zc_data/jx_0217/original/data/wujian/save_loujian_che_1200_5_result'


# label_path = "/mnt/data3/zc_data/jx_0217/original/data/loujian/loujian_lvmo_labels"
# json_path = "/mnt/data3/zc_data/jx_0217/original/data/loujian/loujian_lvmo_labels.json"
# img_path = "/mnt/data3/zc_data/jx_0217/original/data/images"
# output_img_path = '/mnt/data3/zc_data/jx_0217/original/data/loujian/result_img_lvmo'



if not os.path.exists(output_img_path):
    os.makedirs(output_img_path)


txt_list = os.listdir(label_path)
print(txt_list, label_path)

cls_list = ["tower", "crane",  "excavator"]
# cls_list = ['green_net']

output = []

for txt_name in tqdm(txt_list):
    json_data = {}
    json_data['original_image'] = txt_name.replace('txt', 'jpeg')
    img_name = os.path.join(img_path, txt_name.replace('txt', 'jpeg'))
    img = cv2.imread(img_name)
    h, w, c = img.shape

    f = open(os.path.join(label_path, txt_name), 'r')
    lines = f.readlines()
    out = []
    for i, line in enumerate(lines):
        json_data_result = {}
        img1 = img.copy()
        line = line.split(' ')
        print(line)
        cls = int(float(line[0]))
        w_b = float(line[3])*w
        h_b = float(line[4])*h

        x, y = float(line[1])*w-0.5*w_b, float(line[2])*h-0.5*h_b
        class_name = cls_list[cls]
        result_name = txt_name.split(".")[0]+'_{}_{}.jpeg'.format(class_name, i)

        cv2.rectangle(img1, (int(x), int(y)), (int(x+w_b), int(y+h_b)), (0, 0, 255), 3)
        cv2.imwrite(os.path.join(output_img_path, result_name), img1)

        json_data_result['result_image'] = result_name
        json_data_result['label_id'] = cls+1155
        json_data_result['name'] = class_name
        json_data_result['box'] = [int(x), int(y), int(w_b), int(h_b)]
        json_data_result['score'] = random.randint(70, 95)*0.01
        out.append(json_data_result)
    json_data["result"] = out

    output.append(json_data)
with open(json_path, 'w') as json_fp:
    json_str = json.dumps(output, indent=4)
    json_fp.write(json_str)

    #     print(line)
    # img_name = txt_name.replace('txt', 'jpeg')
    # json_data['name'] = img_name
    # json_data['box'] = lines
    # exit()

