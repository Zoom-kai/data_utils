import cv2
import numpy as np
import os
# 定义相关路径
img_path = 'image.jpg'
yolo_out_path = 'yolo_output.txt'
label_path = 'label.txt'
lemon_color = (0, 255, 0)
apple_color = (0, 0, 255)
missed_dir = 'missed'
false_dir = 'false'
# 读取yolo输出结果
yolo_out = np.loadtxt(yolo_out_path)
# 读取标签文件
with open(label_path, 'r') as f:
    lines = f.readlines()
labels = []
for line in lines:
    label = line.strip().split(' ')
    label[1:] = [float(x) for x in label[1:]]
    labels.append(label)
# 将标签文件中的坐标转为[x_min, y_min, x_max, y_max]
for label in labels:
    x_center, y_center, width, height = label[1:]
    x_min, y_min = int((x_center - width / 2) * img.shape[1]), int((y_center - height / 2) * img.shape[0])
    x_max, y_max = int((x_center + width / 2) * img.shape[1]), int((y_center + height / 2) * img.shape[0])
    label[1:] = [x_min, y_min, x_max, y_max]
# 匹配和绘制框
for out in yolo_out:
    found = False
    for label in labels:
        if out[4] == label[0]:
            iou = box_iou(out[:4], label[1:])
            if iou > 0.5:
                found = True
                class_name = label[0]
                x_min, y_min, x_max, y_max = label[1:]
                # 绘制标签框
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), lemon_color, 2)
                # 绘制检测框
                x_min, y_min, x_max, y_max = out[:4]
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), apple_color, 2)
                break
    if not found:
        # 没找到匹配的标签框，将其保存到missed&lowbar;dir
        x_min, y_min, x_max, y_max = out[:4]
        roi = img[y_min:y_max, x_min:x_max]
        cv2.imwrite(os.path.join(missed_dir, f'{class_name}.jpg'), roi)
# 检查漏检和误检的情况
for label in labels:
    found = False
    for out in yolo_out:
        if out[4] == label[0]:
            iou = box_iou(out[:4], label[1:])
            if iou > 0.5:
                found = True
                break
    if not found:
        # 没找到匹配的检测框，将其保存到missed&lowbar;dir
        x_min, y_min, x_max, y_max = label[1:]
        roi = img[y_min:y_max, x_min:x_max]
        cv2.imwrite(os.path.join(missed_dir, f'{label[0]}.jpg'), roi)
for out in yolo_out:
    found = False
    for label in labels:
        if out[4] == label[0]:
            iou = box_iou(out[:4], label[1:])
            if iou > 0.5:
                found = True
                break
    if not found:
        # 没找到匹配的标签框，将其保存到false&lowbar;dir
        x_min, y_min, x_max, y_max = out[:4]
        roi = img[y_min:y_max, x_min:x_max]
        cv2.imwrite(os.path.join(false_dir, f'{class_names[int(out[4])]}.jpg'), roi)
# 计算IOU的函数
def box_iou(box1, box2):
    x1, y1, x2, y2 = box1
    w1, h1 = x2 - x1, y2 - y1
    x1, y1, x2, y2 = box2
    w2, h2 = x2 - x1, y2 - y1
    inter = min(w1, w2) * min(h1, h2)
    iou = inter / (w1 * h1 + w2 * h2 - inter)
    return iou
# 显示图片
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()