import  os
import shutil
from tqdm import tqdm
from shutil import copy2

# 图片路径
img_path = "/mnt/data1/zc_data/open_source_biandianzhan/gongzhuangshibie/images/train"

# 寻找对应图片labels路径
label_path = "/mnt/data1/zc_data/open_source_biandianzhan/gongzhuangshibie/labels/train_4"

# 保存对应labels的路径
new_labels_path = "/mnt/data1/zc_data/open_source_biandianzhan/gongzhuangshibie/labels/train_2"

# labels 类型
labels_end = "txt"

if not os.path.exists(new_labels_path):
    os.makedirs(new_labels_path)

img_list = os.listdir(img_path)
a = 0
print(img_list)
for img_name in tqdm(img_list):

    print(img_name)
    img = os.path.join(img_path, img_name)


    print(img)
    img_end = img_name.split(".")[-1]

    label = os.path.join(label_path, img_name.replace(img_end, labels_end))

    if os.path.exists(label):

        copy2(label, new_labels_path)
        a += 1
        print(a)