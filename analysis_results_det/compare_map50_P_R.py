import glob
import os
import numpy as np


def load_annotations(annotation_dir):
    annotations = {}
    print(glob.glob(os.path.join(annotation_dir, "*.txt")))
    for annotation_file in glob.glob(os.path.join(annotation_dir, "*.txt")):
        print(annotation_file)
        with open(annotation_file, "r") as file:
            lines = file.readlines()
        annotations[annotation_file] = [line.strip().split() for line in lines]
    return annotations
def calculate_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    left = max(x1 - w1/2, x2 - w2/2)
    top = max(y1 - h1/2, y2 - h2/2)
    right = min(x1 + w1/2, x2 + w2/2)
    bottom = min(y1 + h1/2, y2 + h2/2)
    intersection = max(0, right - left) * max(0, bottom - top)
    area1 = w1 * h1
    area2 = w2 * h2
    iou = intersection / (area1 + area2 - intersection)
    return iou
def calculate_metrics(annotation_dir1, annotation_dir2, threshold):
    annotations1 = load_annotations(annotation_dir1)
    annotations2 = load_annotations(annotation_dir2)
    num_annotations1 = sum(len(annotation_list) for annotation_list in annotations1.values())
    num_annotations2 = sum(len(annotation_list) for annotation_list in annotations2.values())
    tp = 0  # True positives
    fp = 0  # False positives
    fn = 0  # False negatives
    print(annotations1)
    for path, annotations1_list in annotations1.items():
        print(annotations1_list)
        annotations2_list = annotations2.get(path, [])
        num_annotations1_list = len(annotations1_list)
        num_annotations2_list = len(annotations2_list)
        for annotation1 in annotations1_list:
            max_iou = 0
            for annotation2 in annotations2_list:
                iou = calculate_iou(annotation1[1:], annotation2[1:])
                if iou > max_iou:
                    max_iou = iou
            if max_iou >= threshold:
                tp += 1
            else:
                fp += 1
        fn += num_annotations2_list - tp
    print(tp, fp, fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1_score = (2 * precision * recall) / (precision + recall)
    return precision, recall, f1_score
# Example usage
annotation_dir1 = "/mnt/data1/zc_code/yolov5_v7.0/runs/detect/smoke_det_cls_test_0601_quantian_0629/labels"  # 第一个标签文件夹路径
annotation_dir2 = "/mnt/data1/zc_data/smoke_data/smoke_wufu/labels/val"  # 第二个标签文件夹路径


threshold = 0.5  # IOU 阈值
precision, recall, f1_score = calculate_metrics(annotation_dir1, annotation_dir2, threshold)
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1_score}")