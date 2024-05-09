import os
from tqdm import tqdm

txt_path = "/mnt/data1/zc_data/anquandai/labels/train_b"   # txt文件所在路径
new_txt_path = "/mnt/data1/zc_data/anquandai/labels/train_s"

# /mnt/data3/zc_data/che_gdj/data_gdj_diaoche
def xyxy2xywh(bbox):
    return [
        (bbox[0]+bbox[2])*0.5,
        (bbox[1]+bbox[3])*0.5,
        bbox[2]-bbox[0],
        bbox[3]-bbox[1],
    ]

def xywh2xyxy(bbox):
    return [
        bbox[0]-0.5*bbox[2],
        bbox[1]-bbox[3]*0.5,
        bbox[2]*0.5+bbox[0],
        bbox[3]*0.5+bbox[1],
    ]

class_num = 3  # 样本类别数
class_list = [i for i in range(class_num)]
class_num_list = [0 for i in range(class_num)]
labels_list = os.listdir(txt_path)
for i in tqdm(labels_list):
    file_path = os.path.join(txt_path, i)
    new_file_path = os.path.join(new_txt_path, i)

    file = open(file_path, 'r')  # 打开文件
    new_file = open(new_file_path, "w")

    file_data = file.readlines()  # 读取所有行
    for line in file_data:
        line_s = line.rstrip().split(' ')
        # print(line_s)
        if line_s[0] == '1':
            h = float(line_s[-1])*0.33
            w = float(line_s[-2])*0.85
            cy = float(line_s[2]) - 0.5*h
            cx = line_s[1]
            cls = 1
        else:
            cls, cx, cy, w, h = line_s
        new_file.write("{} {} {} {} {}\n".format(cls, cx, cy, w, h))

    file.close()
    new_file.close()
