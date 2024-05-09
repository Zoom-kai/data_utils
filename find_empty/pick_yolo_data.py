import os
from tqdm import tqdm
from shutil import copy
import shutil


data_path = "/mnt/data1/zc_data/dianchang/dianchang_05_data/weilan/"
save_path = "/mnt/data1/zc_data/dianchang/dianchang_05_data/weilan/"

img_path = os.path.join(data_path, "images/val")

# img_path = "/mnt/data1/zc_data/dianchang/dianchang_5yue/dianchang_all_0613_img_ori_7049/"

txt_path = os.path.join(data_path, "labels/val_old")

# 保存挑选出来数据的存放路径
new_txt_path = os.path.join(save_path, "labels/val")
new_img_path = os.path.join(save_path, "images")


#原始数据路径
# data_path = "/mnt/data1/zc_data/open_source_biandianzhan/gongzhuangshibie/"

# img_path = os.path.join(data_path, "images/train")
# txt_path = os.path.join(data_path, "labels/train_4")

# # 保存挑选出来数据的存放路径
# new_txt_path = os.path.join(data_path, "labels/train_2")
# new_img_path = os.path.join(data_path, "images/dianchang_2")

# 标签文件的尾缀
labels_end = 'txt'

# 是否重新排序
resort_label = True

# 需要挑选的类别id, 有多个就写多个
label_id = [0, 1, 2, 3]

l = len(label_id)
new_label_id = list(range(l))
# new_label_id = [1, 0]

img_name_list = os.listdir(img_path)
if not os.path.exists(new_txt_path):
    os.makedirs(new_txt_path)

if not os.path.exists(new_img_path):
    os.makedirs(new_img_path)

pic_num = 0
for name in img_name_list:
    pic_num += 1
    print(pic_num)
    # if pic_num > 4000:
    #     exit()
    print(name)
    img_end = name.split('.')[-1]
    txt_name = name.replace(img_end, labels_end)
    if not os.path.exists(os.path.join(txt_path, txt_name)):

        continue
    f = open(os.path.join(txt_path, txt_name), "r")
    lines0 = f.readlines()
    # lines = [_ for _ in f.readlines() if int(_[:2]) in label_id]
    lines = []
    for l in lines0:
        # print(l)
        l0 = l
        l = l.split(" ")
        if int(l[0]) in label_id:
            lines.append(l0)

    # print(txt_name)
    # print(lines)
    if lines == []:
        print(8888888888888888888888888888888)
        continue

    # data = f.readlines()
    with open(os.path.join(new_txt_path, txt_name), "w") as new_txt:
        for line in lines:
            line = line.rstrip().split(' ')
            # print(line)
            if int(line[0]) in label_id:
                cls, cx, cy, w, h = line

                # person2aqd
                # h = float(h)
                # cy = float(cy)
                # h = 0.7*h
                # cy = cy-h*0.1
                # if cls == 2:
                #
                #     h_ori = float(h)
                #     cy_ori = float(cy)
                #     h = 1.8*h_ori
                #     cy = cy_ori+h*0.5
                #     if (cy + 0.5*h) > 1:
                #         cy = cy_ori
                #         h = h_ori

                if resort_label:
                    idx = label_id.index(int(cls))
                    cls = new_label_id[idx]

                # if cls == 0:
                #     if float(1/float(w)) > 20 or float(1/float(h)) > 20:
                #         continue

                # if cls == 2:
                #     if float(1/float(w)) > 12.8 or float(1/float(h)) > 16:
                #         continue


                print(line)
                new_txt.write("{} {} {} {} {}\n".format(cls, cx, cy, w, h))

    # print(new_txt.readlines())
    new_txt.close()
    f.close()

    # old_img = os.path.join(img_path, name)
    # copy(old_img, new_img_path)
    #
    # copy(old_img, new_img_path)



