import os
from tqdm import tqdm

txt_path = "/mnt/data1/zc_data/dianchang/dianchang_06/haitian_0626/labels"   # txt文件所在路径
class_num = 22  # 样本类别数
class_list = [i for i in range(class_num)]
class_num_list = [0 for i in range(class_num)]
labels_list = os.listdir(txt_path)
for i in labels_list:
    file_path = os.path.join(txt_path, i)
    file = open(file_path, 'r')  # 打开文件
    file_data = file.readlines()  # 读取所有行
    for every_row in file_data:
        class_val = every_row.split(' ')[0]
        class_val = float(class_val)
        class_ind = class_list.index(int(class_val))
        class_num_list[class_ind] += 1
    file.close()
# 输出每一类的数量以及总数
print(class_num_list)
print('total:', sum(class_num_list))




