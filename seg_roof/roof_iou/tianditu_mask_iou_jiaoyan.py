import cv2
import torch
from tqdm import tqdm
import numpy as np
import os
import matplotlib.pyplot as plt
from contours import figure_num



def check_label(tianditu_mask, mask, img, out_save_path_map, out_save_path_mask, label=1):
    pictue_size = tianditu_mask.shape
    picture_height = pictue_size[0]
    picture_width = pictue_size[1]

    # plt.imshow(img)
    # plt.show()
    tianditu_mask[tianditu_mask == label] = 255

    ######################边界提取，contours包含边界值的坐标
    contours, hierarchy = cv2.findContours(tianditu_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    tianditu_mask2 = [0 for i in range(len(contours))]
    # print(len(contours))
    background = np.zeros((tianditu_mask.shape[0], tianditu_mask.shape[1]), np.uint8)
    for i in range(len(contours)):
        tianditu_mask2[i] = np.zeros((tianditu_mask.shape[0], tianditu_mask.shape[1]), np.uint8)  ############黑色底板图片读取
        # print(tianditu_mask2[i].shape)
        #    cv2.drawContours(tianditu_mask2[i],contours[i],-1,(0,0,255),3)  #########画边界
        ###############全图片遍历找到相应的在轮廓之内的点
        for a in range(picture_height):
            for b in range(picture_width):
                #############################################辨别是否在轮廓内是定义为1，不是定义为-1
                result = cv2.pointPolygonTest(contours[i], (a, b), False)
                if result > 0:
                    tianditu_mask2[i][b, a] = 1
    mask[mask != 0] = 1
    for mask_pic in tianditu_mask2:
        if mask_pic.sum() < 2000:
            continue


        print(mask_pic.sum())
        # mask_pic[mask_pic == 1] = 255
        # plt.imshow(mask_pic)
        # plt.show()
        roof = img
        roof[mask_pic != 1, :] = 0
        # plt.imshow(roof)
        # plt.show()
        # exit()
        # print(roof.shape)

        num, _ = figure_num(roof)
        if num > 5:
            continue
        intersecting_graph = mask_pic & mask
        if intersecting_graph.__contains__(True) is False:
            img[mask_pic == 1, :] = 0

        iou = intersecting_graph.sum() / min(mask_pic.sum(), mask.sum())
        if iou > 0.5:
            background = background + mask_pic
            # background[background == 1] = 255
        else:
            img[mask_pic == 1, :] = 0
    duoyude = mask - background
    img[duoyude == 1, :] = 0
    # plt.imshow(img)
    # plt.show()

    background[background == 1] = 255

    return img, background



def crop_roof_from_satellite_image(satellite_map_path, locations, save_path_new_mask, save_path_img_patch, img, save_img_patch_path):
    if not os.path.isdir(save_path_img_patch):
        os.mkdir(save_path_img_patch)
    if not os.path.isdir(save_path_new_mask):
        os.mkdir(save_path_new_mask)


    # satellite_map = cv2.imread(satellite_map_path)

    i = 0
    basename = os.path.basename(satellite_map_path)
    patch_list = []
    # print(len(locations))
    for location_i in locations:

        backgroud = np.zeros((img.shape[0], img.shape[1]))
        # roof = satellite_map[location_i[0]:location_i[1], location_i[2]:location_i[3]]
        # print(location_i[4][location_i[4] != False])
        location_i[4]= location_i[4] + 0
        # print(location_i)
        # roof[location_i[4] == 0] = 0

        mask = location_i[4]
        mask[mask == 1] = 255
        # print(mask, mask.shape, location_i[0],location_i[1], location_i[2],location_i[3])
        out_mask_roof = img[location_i[0]:location_i[1], location_i[2]:location_i[3]]
        # tianditu_roof = mask[location_i[0]:location_i[1], location_i[2]:location_i[3]]
        tianditu_roof = mask

        # plt.imshow(tianditu_roof)
        # plt.show()
        # tianditu_roof[mask == 1] = 255
        # print(tianditu_roof)
        # print(tianditu_roof.shape, out_mask_roof.shape)
        # print(tianditu_roof, out_mask_roof)
        intersecting_graph = tianditu_roof & out_mask_roof
        # print(intersecting_graph.sum(), min(tianditu_roof.sum(), out_mask_roof.sum()))
        iou = intersecting_graph.sum() / min(tianditu_roof.sum(), out_mask_roof.sum())
        # print(iou)
        if iou > 0.3:

            # print(intersecting_graph)
            # print(locations)
            # show result
            font = cv2.FONT_HERSHEY_COMPLEX
            #cv2.putText(tianditu_roof, "{}".format(iou), (0, 0), font, fontScale=1, color=(0,255,0), thickness=1)
            # cv2.imwrite("show_result/tianditu_mask.png", )


            backgroud[location_i[0]:location_i[1], location_i[2]:location_i[3]] = tianditu_roof
            patch_list.append(backgroud)
    new_mask = 0
    for patch in patch_list:
        new_mask += patch

    # cv2.imwrite(os.path.join(save_img_patch_path, basename + '_{}.png'.format(i)), save_img)
    cv2.imwrite(os.path.join(save_path_new_mask, basename), new_mask)
    # cv2.imwrite(os.path.join(save_path_img_patch,basename + '_{}-{}_{}_{}_{}.png'.format(i, location_i[0], location_i[1], location_i[2],location_i[3])), roof)



if __name__ == '__main__':

    out_masks_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/output_result_1101_2048"
    mask_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/masks_patch_s"
    img_path = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/images_patch"

    out_save_path_mask = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/jiaoyan_mask"
    out_save_path_map = "/mnt/data1/zc_data/map_data/tianditu_merge/ori_ditu/tianditu_data4_1101/jiaoyan_map"

    tianditu_mask_list = os.listdir(mask_path)
    new_list = os.listdir(out_save_path_mask)

    if not os.path.exists(out_save_path_mask):
        os.makedirs(out_save_path_mask)
    if not os.path.exists(out_save_path_map):
        os.makedirs(out_save_path_map)

    for img_name in tqdm(tianditu_mask_list):
        # if img_name in new_list:
        #     continue
        mask = "{}/{}".format(mask_path, img_name)
        map_path = "{}/{}".format(img_path, img_name)

        if not os.path.exists(map_path):
            continue

        imoutput_mask = cv2.imread("{}/{}".format(out_masks_path, img_name), cv2.IMREAD_GRAYSCALE)
        tianditu_mask = cv2.imread(mask, cv2.IMREAD_GRAYSCALE)
        map_img = cv2.imread(map_path)

        img, mask = check_label(tianditu_mask, imoutput_mask, map_img, out_save_path_map, out_save_path_mask)

        cv2.imwrite(os.path.join(out_save_path_mask, img_name), mask)
        cv2.imwrite(os.path.join(out_save_path_map, img_name), img)

