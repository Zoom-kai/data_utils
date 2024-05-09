import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
from PIL import Image
#from skimage import io
import random
from PIL import Image
from tqdm import tqdm
from contours import figure_num



##### 代码有BUG 待修复 ##############################


def delete_small_roof(mask, img, little_roof, name, label=1):
    pictue_size = mask.shape
    picture_height = pictue_size[0]
    picture_width = pictue_size[1]

    # mask[mask == label] = 255

    ######################边界提取，contours包含边界值的坐标
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    img2 = [0 for i in range(len(contours))]
    # print(len(contours))

    h, w, c = img.shape
    background = np.zeros((mask.shape[0], mask.shape[1]), np.uint8)


    for i in range(len(contours)):

        img2[i] = np.zeros((mask.shape[0], mask.shape[1]), np.uint8)  ############黑色底板图片读取
        # print(img2[i].shape)
        #    cv2.drawContours(img2[i],contours[i],-1,(0,0,255),3)  #########画边界
        ###############全图片遍历找到相应的在轮廓之内的点

        for point in contours[i]:
            if 0  in point[0] or h-1 in point[0] or w-1 in point[0]:
                # print(point[0])
                p.append(point[0])
                # print("pppppppp: ", p)
                # print("len(p): {}".format(len(p)))

        p = []
        if p != [] and len(p) != 1:
            # print(p)
            if p[0][0] != p[1][0] and p[0][1] != p[1][1]:
                if p[0][0] == p[1][1]:
                    cv2.line(img2[i], (p[0][0], p[0][1]), (p[0][0], p[0][0]), 1, 1)
                    cv2.line(img2[i], (p[1][0], p[1][1]), (p[0][0], p[0][0]), 1, 1)

                elif p[0][1] == p[1][0]:
                    cv2.line(img2[i], (p[0][0], p[0][1]), (p[0][1], p[0][1]), 1, 1)
                    cv2.line(img2[i], (p[1][0], p[1][1]), (p[0][1], p[0][1]), 1, 1)
            else:
                cv2.line(img2[i], (p[0][0], p[0][1]), (p[1][0], p[1][1]), 1, 1)

        cv2.drawContours(img2[i],contours,i,1, 1)



    for mask_pic in img2:
        # print(mask_pic.sum())


        # if mask_pic.sum() < 2000:
        #     continue
        roof = img
        roof[mask_pic != 1, :] = 0
        num, _ = figure_num(roof)
        # print(num)
        # plt.imshow(roof)
        # plt.show()

        if num > 50:
            print(name, num)
            cv2.imwrite(os.path.join(little_roof, "{}_{}".format(num, name)), roof)
            continue

        background = background + mask_pic
        # background[background == 1] = 1

    return background



if __name__ == '__main__':
    mask_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/masks_patch"
    new_mask_save_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/masks_patch"
    img_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/images_patch"

    little_roof = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/small_roof"

    if not os.path.exists(new_mask_save_path):
        os.makedirs(new_mask_save_path)

    if not os.path.exists(little_roof):
        os.makedirs(little_roof)

    mask_names = os.listdir(mask_path)
    np.random.shuffle(mask_names)

    for name in tqdm(mask_names):
        new_mask_names = os.listdir(new_mask_save_path)
        if name in new_mask_names:
            continue
        # print(name)
        mask = cv2.imread(os.path.join(mask_path, name), cv2.IMREAD_GRAYSCALE)   ############图片读取

        if not os.path.exists(os.path.join(img_path, name)):
            continue
        img = cv2.imread(os.path.join(img_path, name))   ############图片读取

        new_mask = delete_small_roof(mask, img, little_roof, name)

        cv2.imwrite(os.path.join(new_mask_save_path, name), new_mask)



















