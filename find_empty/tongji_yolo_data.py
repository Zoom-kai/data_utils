import os
from tqdm import tqdm
from shutil import copy

#原始数据路径
img_path = "D:\datasets\daiyanshou\jiangxi_jinglianwen_01\images/"
txt_path = "D:\datasets\daiyanshou\jiangxi_jinglianwen_01\labels/"

# 保存挑选出来数据的存放路径
# new_txt_path = "/mnt/data1/zc_data/jueyuanzi/wushan/labels_jueyuanzi/train"
# new_img_path = "/mnt/data1/zc_data/jueyuanzi/wushan/images_jueyuanzi/train"

# 标签文件的尾缀
labels_end = 'txt'

# 是否重新排序
resort_label = True

# 需要挑选的类别id, 有多个就写多个
# label_id = [0]

# l = len(label_id)
# new_label_id = list(range(l))


img_name_list = os.listdir(img_path)

n_obj = 0

for name in img_name_list:
    img_end = name.split('.')[-1]
    txt_name = name.replace(img_end, labels_end)
    if not os.path.exists(os.path.join(txt_path, txt_name)):
        continue
    f = open(os.path.join(txt_path, txt_name), "r")
    # lines = [_ for _ in f.readlines() if int(_[0]) in label_id]
    lines = f.readlines()
    # print(lines)
    if lines == []:
        continue

    # data = f.readlines()

    for line in lines:
        line = line.rstrip().split(' ')

        cls, cx, cy, w, h = line

        n_obj += 1

print("num obj: {}".format(n_obj))






