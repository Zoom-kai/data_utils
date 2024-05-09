import cv2
import torch
from tqdm import tqdm
import numpy as np
import os
import matplotlib.pyplot as plt

def split_mask(mask, use_cuda=False, width_thresh= 10, height_thresh=10,area_thresh=400,resolution = 0.59, cuda_id = 3):
    # gray = cv2.cvtColor(img_zeros, cv2.COLOR_BGR2GRAY)
    mask = cv2.imread(mask, cv2.IMREAD_GRAYSCALE)
    ret, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 定义结构元素的形状和大小
    dst = cv2.erode(binary, kernel)
    dst = cv2.dilate(dst, kernel)

    _, instances = cv2.connectedComponents(dst)
    # _, labels, instances, centroids = cv2.connectedComponentsWithStats(dst, ltype=cv2.CV_16U)
    # mask[mask==1] = 255
    # plt.imshow(mask)
    # plt.show()


    pbar = total=tqdm(instances.max())
    # for instance_i_num in range(1, instances.max()):
    locations = []
    if use_cuda:
        instances = torch.from_numpy(instances).to('cuda:{}'.format(cuda_id))
        for instance_i_num in range(1, instances.max()):
            index = instances == instance_i_num
            index_center_x, index_center_y = torch.where(index)
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

    out_masks_path = "/mnt/data1/zc_data/map_data/tianditu_data/output_old_model_pitch"
    mask_path = "/mnt/data1/zc_data/map_data/tianditu_data/labels"
    save_path_mask = "/mnt/data1/zc_data/map_data/tianditu_data/labels_roof_iou_1013"
    save_path_img = "little_mask/"

    tianditu_mask_list = os.listdir(mask_path)
    if not os.path.exists(save_path_mask):
        os.makedirs(save_path_mask)
    for img_name in tqdm(tianditu_mask_list):

        imoutput_mask = cv2.imread("{}/{}".format(out_masks_path, img_name), cv2.IMREAD_GRAYSCALE)
        mask = "{}/{}".format(mask_path, img_name)

        map_path = "{}/{}".format(out_masks_path, img_name)
        print(mask)
        locations = split_mask(mask, use_cuda=True)
        crop_roof_from_satellite_image(map_path, locations, save_path_mask, save_path_img, imoutput_mask, save_path_img)


