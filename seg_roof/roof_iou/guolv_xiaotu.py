
# 用来过滤过小的屋顶 mask

import cv2
import torch
from tqdm import tqdm
import numpy as np
import os
import matplotlib.pyplot as plt
from contours import figure_num

def split_mask(mask, use_cuda=False, width_thresh=30, height_thresh=30,area_thresh=1000,resolution = 0.59, cuda_id = 3):
    # gray = cv2.cvtColor(img_zeros, cv2.COLOR_BGR2GRAY)
    mask = cv2.imread(mask, cv2.IMREAD_GRAYSCALE)

    plt.imshow(mask)
    plt.show()

    ret, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)


    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 定义结构元素的形状和大小
    dst = cv2.erode(binary, kernel)
    dst = cv2.dilate(dst, kernel)

    plt.imshow(dst)
    plt.show()

    _, instances = cv2.connectedComponents(dst)
    print(len(instances))
    # _, labels, instances, centroids = cv2.connectedComponentsWithStats(dst, ltype=cv2.CV_16U)
    # mask[mask==1] = 255
    # plt.imshow(mask)
    # plt.show()

    pbar = total = tqdm(instances.max())
    # for instance_i_num in range(1, instances.max()):
    locations = []
    if use_cuda:
        instances = torch.from_numpy(instances).to('cuda:{}'.format(cuda_id))
        for instance_i_num in range(1, instances.max()):
            index = instances == instance_i_num
            print(index)
            print(index[index!= False])
            index_center_x, index_center_y = torch.where(index)
            print(index_center_x, index_center_y)
            print(torch.where(index))

            exit()
            index_x_min = index_center_x.min()
            index_x_max = index_center_x.max()
            index_y_min = index_center_y.min()
            index_y_max = index_center_y.max()
            local_index = index[index_x_min:index_x_max, index_y_min:index_y_max]
            height = index_center_x.max() - index_center_x.min()
            width = index_center_y.max() - index_center_y.min()
            pbar.update(1)
            if width < width_thresh or height < height_thresh:
                # instances[index] = 0
                # dst[index] = 0
                continue
            area = index.sum() * (resolution ** 2)
            if area < area_thresh:
                # instances[index] = 0
                # dst[index] = 0
                continue
            locations.append(
                [index_x_min.cpu().numpy(), index_x_max.cpu().numpy(), index_y_min.cpu().numpy(), index_y_max.cpu().numpy(),
                 local_index.cpu().numpy()])
    else:
        for instance_i_num in range(1, instances.max()):
            index = instances == instance_i_num
            index_center_x, index_center_y = np.where(index)
            index_x_min = index_center_x.min()
            index_x_max = index_center_x.max()
            index_y_min = index_center_y.min()
            index_y_max = index_center_y.max()
            local_index = index[index_x_min:index_x_max, index_y_min:index_y_max]
            height = index_center_x.max() - index_center_x.min()
            width = index_center_y.max() - index_center_y.min()
            pbar.update(1)
            if width < width_thresh or height < height_thresh:
                instances[index] = 0
                dst[index] = 0
                continue
            area = index.sum() * (resolution ** 2)
            if area < area_thresh:
                instances[index] = 0
                dst[index] = 0
                continue
            locations.append([index_x_min, index_x_max, index_y_min, index_y_max, local_index])
    pbar.close()
    return locations

def crop_roof_from_satellite_image(satellite_map_path, locations, save_path_new_mask, save_path_img_patch, img, save_img_patch_path):
    if not os.path.isdir(save_path_img_patch):
        os.mkdir(save_path_img_patch)
    if not os.path.isdir(save_path_new_mask):
        os.mkdir(save_path_new_mask)


    satellite_map = cv2.imread(satellite_map_path)

    i = 0
    basename = os.path.basename(satellite_map_path)
    patch_list = []

    for location_i in locations:

        backgroud = np.zeros((img.shape[0], img.shape[1]))

        mask = location_i[4] + 0


        mask[mask == 1] = 255

        plt.imshow(mask)
        plt.show()

        tianditu_roof = mask
        roof = satellite_map[location_i[0]:location_i[1], location_i[2]:location_i[3]]
        roof_num, contours = figure_num(roof)
        print("roof_num:{}".format(roof_num))
        if roof_num > 5:
            continue
        backgroud[location_i[0]:location_i[1], location_i[2]:location_i[3]] = tianditu_roof
        patch_list.append(backgroud)

    new_mask = 0
    for patch in patch_list:
        new_mask += patch

    # cv2.imwrite(os.path.join(save_img_patch_path, basename + '_{}.png'.format(i)), save_img)
    cv2.imwrite(os.path.join(save_path_new_mask, basename), new_mask)

    plt.imshow(new_mask)
    plt.show()



    # cv2.imwrite(os.path.join(save_path_img_patch,basename + '_{}-{}_{}_{}_{}.png'.format(i, location_i[0], location_i[1], location_i[2],location_i[3])), roof)



if __name__ == '__main__':

    map_path = "/mnt/data1/zc_data/map_data/train_20k_old_map/images/train"
    mask_path = map_path.replace("images", "masks")

    save_path_mask = mask_path.replace("masks", "masks_not_little")
    save_path_img = map_path.replace("images", "images_not_little")


    tianditu_mask_list = os.listdir(mask_path)
    if not os.path.exists(save_path_mask):
        os.makedirs(save_path_mask)

    if not os.path.exists(save_path_img):
        os.makedirs(save_path_img)

    for img_name in tqdm(tianditu_mask_list):

        imoutput_mask = cv2.imread("{}/{}".format(map_path, img_name))
        mask = "{}/{}".format(mask_path, img_name)

        map = "{}/{}".format(map_path, img_name)
        # print(mask)
        locations = split_mask(mask, use_cuda=True)
        crop_roof_from_satellite_image(map, locations, save_path_mask, save_path_img, imoutput_mask, save_path_img)



