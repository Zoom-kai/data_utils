import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


# img_path = "/mnt/data1/zc_data/peidianfang/peidianfang_1222/coco/images/train2017"
# label_path = "/mnt/data1/zc_data/peidianfang/peidianfang_1222/coco/labels/train2017"
# save_path = "/mnt/data1/zc_data/peidianfang/peidianfang_1222/coco/pose_label_preview"
img_path = "/mnt/data1/zc_data/dianchang/dianchang_5yue/aqd_pose/images"
label_path = "/mnt/data1/zc_data/dianchang/dianchang_5yue/aqd_pose/labels/"
save_path = "/mnt/data1/zc_data/dianchang/dianchang_5yue/aqd_pose/labels_preview_aqd_pose_0622"


if not os.path.exists(save_path):
    os.makedirs(save_path)

radius = 5
img_names = os.listdir(img_path)
for name in img_names:
    print(name)
    label_name = name.replace(name.split(".")[1], "txt")
    img = cv2.imread("{}/{}".format(img_path, name))
    h, w, c = img.shape
    f = open("{}/{}".format(label_path, label_name), 'r')
    lines = f.readlines()
    if name[-7:] == "DYB.png":
        for line in lines:
            # print(line)
            line = line.split(" ")
            # lines_arr = np.array(line)
            # print(lines_arr)
            print(555555555555555555555555555555)
            points = line[5:92]
            # print(int(len(points) / 3))
            for i in range(int(len(points) / 3)):
                point = points[i * 3: i * 3 + 2]

                x_coord, y_coord = float(point[0]) * w, float(point[1]) * h
                print(x_coord, y_coord)
                cv2.circle(img, (int(x_coord), int(y_coord)), radius, (int(255), int(0), int(125)), -1)
            # print(points)
            cv2.imwrite("{}/{}".format(save_path, name), img)
            # plt.imshow(img)
            # plt.show()
    else:
        for line in lines:
            print(line)
            line = line.split(" ")
            # lines_arr = np.array(line)
            # print(lines_arr)
            kpt = line[5:]
            cls = int(float(line[0]))
            color = (255, 0, 0)
            if cls == 1:
                color = (0, 0, 255)
            # x = line[6:101], line[92:101]
            for i in range(int(len(kpt)/3)):
                x, y = kpt[i*3:3*i+2]

                x_coord, y_coord = float(x)*w, float(y)*h
                print(x_coord, y_coord)
                cv2.circle(img, (int(x_coord), int(y_coord)), radius, color, -1)
            # print(points)
            cv2.imwrite("{}/{}".format(save_path, name), img)
            # plt.imshow(img)
            # plt.show()


    f.close()
