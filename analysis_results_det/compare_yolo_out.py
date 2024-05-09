import os
import cv2
import random
import string
from openpyxl import Workbook
from tqdm import tqdm

# 定义标签类别，可以根据实际情况进行修改
classes = ['ground', 'offground']

# 设定不同类别的颜色
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]
# 生成随机字符串，用来给临时文件命名
# def random_string(n=8):
#     return '.join(random.choices(string.ascii_letters + string.digits, k=n))

# 从文件中读取标注信息
def read_annotation_file(file):
    objects = []
    with open(file, 'r') as f:
        for line in f:
            object_ = {}
            label, x, y, w, h = line.split()
            object_['label'] = label
            object_['box'] = (x, y, w, h)
            objects.append(object_)
    return objects
# 从文件中读取检测结果
def read_detection_file(file):
    objects = []
    with open(file, 'r') as f:
        for line in f:
            label, left, top, right, bottom = line.split()
            objects.append({'label': label, 'box': (left, top, right, bottom)})
    return objects
# 获取标注和检测结果中所有的不同标签
def get_labels(annotations, detections):
    annotations_labels = set(o['label'] for objects in annotations for o in objects)
    detections_labels = set(o['label'] for objects in detections for o in objects)
    return sorted(annotations_labels.union(detections_labels))
# 读取图像
def read_image(image_file):
    return cv2.imread(image_file)
# 将标注信息和检测结果画到图像上
def draw_on_image(image, objects, color):
    for object_ in objects:
        left, top, right, bottom = object_['box']
        cv2.rectangle(image, (int(left), int(top)), (int(right), int(bottom)), color, 2)

# 比较标注和检测结果，并将结果写入excel表格，并将标注和检测结果画到图像上
def compare_detection_results(annotation_file, detection_file, image_file, name=None):
    annotations = read_annotation_file(annotation_file)
    detections = read_detection_file(detection_file)
    image = read_image(image_file)
    labels = get_labels(annotations, detections)
    mismatch_count = 0
    output_file = 'output_{}'.format(name) + '.jpg'
    output_file_excel = 'output_{}'.format(name) + '.xlsx'

    wb = Workbook()
    ws = wb.active
    ws.append(['类别', '数量', '颜色'])
    for label_idx, label in enumerate(labels):
        annotation_objects = [o for o in annotations if o['label'] == label]
        detection_objects = [o for o in detections if o['label'] == label]
        if len(annotation_objects) != len(detection_objects):
            mismatch_count += 1
        color = colors[label_idx % len(colors)]
        draw_on_image(image, annotation_objects, color)
        draw_on_image(image, detection_objects, color[::-1]) # 将颜色取反，用来标记检测结果
        # ws.append([label, len(annotation_objects), '#' + ''.join(hex©[2:].rjust(2, '0') for c in color)])
    cv2.imwrite(output_file, image)
    # wb.save(output_file_excel)
    return mismatch_count, output_file, output_file_excel

if __name__ == '__main__':
    imgs_path = "/mnt/data1/zc_data/anquandai/ground_or/ground_or_not/images/val/"
    labels_path = "/mnt/data1/zc_data/anquandai/ground_or/ground_or_not/labels/val/"
    out_labels_path = "/mnt/data1/zc_code/yolov5-6.0/runs/detect/ground_0411/labels"

    img_list = os.listdir(imgs_path)
    for img_name in tqdm(img_list):
        name = img_name.split(".")[0]

        annotation_file = '/{}/{}.txt'.format(labels_path, name)
        detection_file = '/{}/{}.txt'.format(out_labels_path, name)
        image_file = '/{}/{}'.format(imgs_path, img_name)

        mismatch_count, output_image_file, output_excel_file = compare_detection_results(annotation_file, detection_file, image_file, name)
        if mismatch_count > 0:
            print(f'有{mismatch_count}个标注与检测结果不匹配，请查看输出的图片和excel文件。')
        else:
            print('标注与检测结果完全匹配。')