import cv2
import os
from tqdm import tqdm

img_path = r"/mnt/data1/zc_data/smoke_data/classify_dataset/smoke_fuyangben/"

labels_path = r"/mnt/data1/zc_code/yolov5-6.0/runs/detect/smoke_0625_fuyangben/labels/"

save_path = r"/mnt/data1/zc_data/smoke_data/classify_dataset/smoke/train/not_smoke"

# save_path = r"/mnt/data1/zc_data/smoke_data/smoke_yolo_merge_0701/smoke_crop_0508_z"

import matplotlib.pyplot as plt

if not os.path.exists(save_path):
    os.makedirs(save_path)

img_list = os.listdir(img_path)

rate = 0.5

delete_small_obj = True

s = 0
for img_name in tqdm(img_list):
    s += 1
    print(s)
    label_file = os.path.join(labels_path, img_name.split(".")[0]+".txt")  # 标签文件路径

    if not os.path.exists(label_file):
        continue

    # if s > 7000:
    #     break
    # 读取标签文件
    with open(label_file, "r") as f:
        lines = f.readlines()

    # 加载图片
    image_path = os.path.join(img_path, img_name)
    image = cv2.imread(image_path)
    h_o, w_o, c = image.shape
    n = 0
    # 循环处理每条标签
    for line in lines:
        print(n)
        values = line.strip().split(" ")

        # boxes = values

        # 处理每个框
        box = values
        # box = list(map(int, box.split(",")))
        box = [float(i) for i in box]



        x, y, w, h = box[1]-box[3]/2, box[2]-box[4]/2, box[3], box[4]  # 转换为左上角坐标和宽高
        x, y, w, h = int(x * w_o), int(y * h_o), int(w * w_o), int(h * h_o)

        print((w_o/w), (h_o/h))
        if delete_small_obj:
            if (w_o/w)>25 and (h_o/h)>25:
                # plt.imshow(image)
                # plt.show()
                continue

        # x, y, w, h = int(x*w_o), int(y*h_o), int(w*w_o), int(h*h_o)



        w, h = int(w+w*rate), int(h+h*rate)

        if w < 224:
            w = 224
        if h < 224:
            h = 224

        if w > w_o:
            w = w_o
        if h > h_o:
            h = h_o

        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if x + w > w_o:
            x = x - (x+w - w_o)
        if y+h > h_o:
            y = y - (y+h - h_o)

        if w == 0 or h == 0:
            continue


        cropped_image = image[y:y+h, x:x+w]  # 截取图片区域
        # 保存图片
        cropped_image_path = os.path.join(
            save_path, img_name.split(".")[0] + "_" + str(box[0]) + str(n) + ".jpg")
        print(cropped_image_path, cropped_image.shape, x,y,w,h, image.shape)
        cv2.imwrite(cropped_image_path, cropped_image)
        n += 1
