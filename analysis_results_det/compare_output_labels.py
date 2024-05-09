import cv2
import torch
import numpy as np
import os

def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    y[0] = x[0] - x[2] / 2  # top left x
    y[1] = x[1] - x[3] / 2  # top left y
    y[2] = x[0] + x[2] / 2  # bottom right x
    y[3] = x[1] + x[3] / 2  # bottom right y
    return y



def box_iou(rec_1, rec_2):
    '''
    rec_1:左上角(rec_1[0],rec_1[1])    右下角：(rec_1[2],rec_1[3])
    rec_2:左上角(rec_2[0],rec_2[1])    右下角：(rec_2[2],rec_2[3])
    （rec_1）
    1--------1
    1   1----1------1
    1---1----1      1
        1           1
        1-----------1 （rec_2）
    '''
    rec_1 = xywh2xyxy(rec_1)
    rec_2 = xywh2xyxy(rec_2)
    s_rec1 = (rec_1[2] - rec_1[0]) * (rec_1[3] - rec_1[1])  # 第一个bbox面积 = 长×宽
    s_rec2 = (rec_2[2] - rec_2[0]) * (rec_2[3] - rec_2[1])  # 第二个bbox面积 = 长×宽
    sum_s = s_rec1 + s_rec2  # 总面积
    left = max(rec_1[0], rec_2[0])  # 并集左上角顶点横坐标
    right = min(rec_1[2], rec_2[2])  # 并集右下角顶点横坐标
    bottom = max(rec_1[1], rec_2[1])  # 并集左上角顶点纵坐标
    top = min(rec_1[3], rec_2[3])  # 并集右下角顶点纵坐标
    if left >= right or top <= bottom:  # 不存在并集的情况
        return 0
    else:
        inter = (right - left) * (top - bottom)  # 求交集面积
        min_rec = min(s_rec1, s_rec2)  # 求两矩形较小面积
        iou = (inter / min_rec) * 1.0  # 计算IOU
        return iou


# 计算所有框的iou和匹配情况
def match_boxes(yolo_out, boxes):
    iou = torch.zeros((yolo_out.shape[0], boxes.shape[0]), dtype=torch.float32)
    for i in range(yolo_out.shape[0]):
        for j in range(boxes.shape[0]):
            iou[i][j] = box_iou(yolo_out[i][1:], boxes[j][1:])

    _, max_indices = iou.max(dim=1)
    matched_boxes = torch.gather(boxes, 0, max_indices.view(-1, 1).repeat(1, boxes.shape[1]).long())

    matched_scores = torch.gather(yolo_out, 0, max_indices.view(-1, 1).repeat(1, yolo_out.shape[1]).long())
    matched_scores = matched_scores[:, [-1]]

    return matched_boxes, matched_scores

if __name__ == '__main__':

    class_names = ["tower", "crane",  "excavator", "truck", "pump_truck"]
    # 定义相关路径
    img_path = '/mnt/data3/zc_data/jx_0217/original/gongchengche_0406/images/val/3f2a9ca5-d639-4267-aeac-661e1832e0fc.jpeg'
    yolo_out_path = '/mnt/data1/zc_code/yolov5-6.0/runs/detect/smoke_0327/labels/3f2a9ca5-d639-4267-aeac-661e1832e0fc.txt'
    label_path = '/mnt/data3/zc_data/jx_0217/original/gongchengche_0406/labels/val/3f2a9ca5-d639-4267-aeac-661e1832e0fc.txt'
    lemon_color = (0, 255, 0)
    apple_color = (0, 0, 255)
    missed_dir = 'output/missed'
    false_dir = 'output/false'

    if not os.path.exists(missed_dir):
        os.makedirs(missed_dir)
    if not os.path.exists(false_dir):
        os.makedirs(false_dir)

    # 读取yolo输出结果
    yolo_out = np.loadtxt(yolo_out_path)
    label_out = np.loadtxt(label_path)

    img = cv2.imread(img_path)
    img_h, img_w = img.shape[:2]

    # 读取标签文件
    with open(label_path, 'r') as f:
        lines = f.readlines()
        labels = []
        for line in lines:
            label = line.strip().split(' ')
            label[1:] = [float(x) for x in label[1:]]
            labels.append(label)
    # 将标签文件中的坐标转为[x_min, y_min, x_max, y_max]
    # for label in labels:
    #     x_center, y_center, width, height = label[1:]
    #     x_min, y_min = int((x_center - width / 2) * img.shape[1]), int((y_center - height / 2) * img.shape[0])
    #     x_max, y_max = int((x_center + width / 2) * img.shape[1]), int((y_center + height / 2) * img.shape[0])
    #     label[1:] = [x_min, y_min, x_max, y_max]

    # 将yolo输出结果转换为PyTorch张量
    yolo_out_tensor = torch.from_numpy(yolo_out).float()
    # 将标签文件转换为PyTorch张量
    # labels_tensor = torch.from_numpy(np.array(labels)).float()
    labels_tensor = torch.from_numpy(np.array(label_out)).float()




    # 并行化计算框的匹配情况
    matched_boxes, matched_scores = match_boxes(yolo_out_tensor, labels_tensor)

    # 匹配上的情况，绘制标签框和检测框
    matched_indices = matched_scores > 0.5
    for i in range(matched_indices.shape[0]):
        if matched_indices[i]:
            class_name = labels[int(matched_boxes[i, 0]), 0]
            x_min, y_min, x_max, y_max = xywh2xyxy(matched_boxes[i, 1:].int())
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), lemon_color, 2)

            x_min, y_min, x_max, y_max = yolo_out_tensor[i, 1:].int()
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), apple_color, 2)
    # 未匹配上的情况，保存漏检图片
    for i in range(yolo_out.shape[0]):
        if not matched_indices[i]:
            x_min, y_min, x_max, y_max = xywh2xyxy(labels[i][1:])
            x_min, y_min, x_max, y_max = x_min*img_w, y_min*img_h, x_max*img_w, y_max*img_h

            roi = img[y_min:y_max, x_min:x_max]
            class_name = class_names[int(yolo_out[i, 0])]


    cv2.imwrite(os.path.join(missed_dir, f'{class_name}.jpg'), roi)
    # 未匹配上的情况，保存误检图片
    for i in range(labels_tensor.shape[0]):
        if not matched_indices[:, i].any():
            x_min, y_min, x_max, y_max = xywh2xyxy(labels[i, 1:])
            x_min, y_min, x_max, y_max = x_min * img_w, y_min * img_h, x_max * img_w, y_max * img_h
            roi = img[y_min:y_max, x_min:x_max]
            class_name = labels[i, 0]
            cv2.imwrite(os.path.join(false_dir, f'{class_name}.jpg'), roi)



    # 显示图片
    cv2.imwrite('output/test.jpg', img)
