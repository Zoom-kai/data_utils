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

def delete_small_roof(mask, img, little_roof, name, label=1):
    pictue_size = mask.shape
    picture_height = pictue_size[0]
    picture_width = pictue_size[1]

    mask[mask == label] = 255

    ######################边界提取，contours包含边界值的坐标
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    img2 = [0 for i in range(len(contours))]
    # print(len(contours))
    background = np.zeros((mask.shape[0], mask.shape[1]), np.uint8)
    for i in range(len(contours)):
        img2[i] = np.zeros((mask.shape[0], mask.shape[1]), np.uint8)  ############黑色底板图片读取
        # print(img2[i].shape)
        #    cv2.drawContours(img2[i],contours[i],-1,(0,0,255),3)  #########画边界
        ###############全图片遍历找到相应的在轮廓之内的点
        for a in range(picture_height):
            for b in range(picture_width):
                #############################################辨别是否在轮廓内是定义为1，不是定义为-1
                result = cv2.pointPolygonTest(contours[i], (a, b), False)
                if result > 0:
                    img2[i][b, a] = 1
    for mask_pic in img2:
        # print(mask_pic.sum())
        if mask_pic.sum() < 1500:
            continue
        roof = img
        roof[mask_pic != 1, :] = 0
        num, _ = figure_num(roof)
        # print(num)
        # plt.imshow(roof)
        # plt.show()

        if num > 5:
            print(name, num)
            cv2.imwrite(os.path.join(little_roof, "{}_{}".format(num, name)), roof)
            continue

        background = background + mask_pic
        # background[background == 1] = 1

    return background



def fill_contours(mask, img, little_roof, name, label=1):
    pictue_size = mask.shape
    picture_height = pictue_size[0]
    picture_width = pictue_size[1]

    mask[mask == label] = 255

    ######################边界提取，contours包含边界值的坐标
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    img2 = [0 for i in range(len(contours))]
    # print(len(contours))
    background = np.zeros((mask.shape[0], mask.shape[1]), np.uint8)
    # for i in range(len(contours)):
    #     img2[i] = np.zeros((mask.shape[0], mask.shape[1]), np.uint8)  ############黑色底板图片读取
    #     # print(img2[i].shape)
    #     #    cv2.drawContours(img2[i],contours[i],-1,(0,0,255),3)  #########画边界
    #     ###############全图片遍历找到相应的在轮廓之内的点
    #     for a in range(picture_height):
    #         for b in range(picture_width):
    #             #############################################辨别是否在轮廓内是定义为1，不是定义为-1
    #             result = cv2.pointPolygonTest(contours[i], (a, b), False)
    #             if result > 0:
    #                 img2[i][b, a] = 1
    for i in range(len(contours)):
        # print(contours[i].shape)
        #
        # plt.imshow(contours[i])
        # plt.show()

        # mask = cv2.drawContours(mask, contours, i, 255, cv2.FILLED)
        mask = cv2.drawContours(mask, contours, i, 255, -1)
        plt.imshow(mask)
        plt.show()

    # exit()

    for mask_pic in img2:
        mask_pic[mask_pic == 255] = 1
        # print(mask_pic.sum())
        if mask_pic.sum() < 2000:
            continue
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


def draw_test():
    import cv2
    import numpy as np

    rows = 512
    cols = 512

    # Create image with new colour for replacement
    img = np.zeros((rows, cols, 3), np.uint8)
    img[:, :] = (0, 0, 0)

    # img=cv2.copyMakeBorder(img,1,1,1,1, cv2.BORDER_CONSTANT, value=[0,0,0])

    # Draw rectangle
    img = cv2.rectangle(img, (400, 0), (512, 100), (255, 255, 255), -1)
    img = cv2.rectangle(img, (0, 400), (512, 100), (255, 255, 255), -1)
    plt.imshow(img)
    plt.show()
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find Contour
    contours, hierarchy = cv2.findContours(imggray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, contours, 0, (0, 0, 255), -1)

    plt.imshow(img)
    plt.show()
    return print(1111111111111)

if __name__ == '__main__':
    mask_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/masks_patch"
    new_mask_save_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/masks_patch_guolv"
    img_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/images_patch"

    little_roof = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/small_roof_1107"

    if not os.path.exists(new_mask_save_path):
        os.makedirs(new_mask_save_path)

    if not os.path.exists(little_roof):
        os.makedirs(little_roof)

    mask_names = os.listdir(mask_path)
    np.random.shuffle(mask_names)

    for name in tqdm(mask_names):
        new_mask_names = os.listdir(new_mask_save_path)
        print(name)
        if name in new_mask_names:
            continue
        # print(name)
        mask = cv2.imread(os.path.join(mask_path, name), cv2.IMREAD_GRAYSCALE)   ############图片读取

        img = cv2.imread(os.path.join(img_path, name))   ############图片读取

        # draw_test()

        new_mask = delete_small_roof(mask, img, little_roof, name)

        # new_mask = fill_contours(mask, img, little_roof, name)    # 边界的轮廓无法填充 ~

        cv2.imwrite(os.path.join(new_mask_save_path, name), new_mask)



















