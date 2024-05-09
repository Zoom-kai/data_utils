
import cv2
import os
import numpy as np
import imutils

save_path = r"ningbo/add_mask_final_center"
img_path = r"/mnt/data1/zc_data/map_data/tianditu_merge/test/ningbo/ningbo_ori"
mask_path = r"ningbo/output_roof"
# mask_path = r"./../utils/new_mask"

img_list = os.listdir(img_path)

for img_name in img_list:
    mask_name = img_name

    img = cv2.imread("{}/{}".format(img_path, img_name))
    mask = cv2.imread("{}/{}".format(mask_path, mask_name), cv2.IMREAD_GRAYSCALE)
    print(mask)
    # mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
    print(mask[mask != 0][mask[mask != 0] != 1])

    mask = cv2.resize(mask, (6185, 5207))
    print(mask.shape, img.shape)
    img[mask != 0, 0] = 255

    # gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)
    thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        # 计算轮廓区域的图像矩。 在计算机视觉和图像处理中，图像矩通常用于表征图像中对象的形状。这些力矩捕获了形状的基本统计特性，包括对象的面积，质心（即，对象的中心（x，y）坐标），方向以及其他所需的特性。
        M = cv2.moments(c)
        # print("M[m10]/M[m00]: {}/{} ".format(M["m10"]), M["m00"])
        # print(M)
        # print(M["m10"], M["m00"])
        if M["m10"]==0 or M["m00"]==0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        S = int(cv2.contourArea(c)*0.51*0.51*0.12)
        # if S==1183:
        #     S = int(S/1.2)
        if S < 30:
            continue
        # print(M)
        # print(c)
        print(cv2.contourArea(c))
        # 在图像上绘制轮廓及中心
        # cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
        # cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(img, "{}KW".format(S), (cX - 10, cY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    print(img.shape)
    print(mask.shape)
    # if os.path.exists("{}/{}".format(img_path, mask_name)) == False:
    #     continue
    if os.path.exists(save_path) == False:
        os.makedirs(save_path)

    # masked = cv2.addWeighted(img.astype(np.uint8), 1, mask.astype(np.uint8), 0.2, gamma=1)

    cv2.imwrite("{}/add_{}".format(save_path, img_name), img)

