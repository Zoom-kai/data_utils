import os

import cv2
import argparse
from tqdm import tqdm


import os
import numpy as np
import cv2
import argparse
from tqdm import tqdm

def convert_mask(mask_path, img_path, label, npy_mask_save_path, npy_img_save_path, name):

    if not os.path.exists(npy_mask_save_path):
        os.makedirs(npy_mask_save_path)
    if not os.path.exists(npy_img_save_path):
        os.makedirs(npy_img_save_path)

    if not os.path.exists(mask_path):
        print("Please input correct mask_path !")

    mask_list = os.listdir(mask_path)

    no_aim_num = 0
    num = 0
    for mask_name in tqdm(mask_list):
        if num % 1 == 0:
            # if mask_name.split(".")[-1] != "tif":
            #     print(mask_name)
            #     continue
            mask = cv2.imread("{}/{}".format(mask_path, mask_name), cv2.IMREAD_GRAYSCALE)
            # print(mask_name)
            img_name = mask_name.split(".")[0]
            img = cv2.imread("{}/{}".format(img_path, mask_name))
            if not os.path.exists("{}/{}".format(mask_path, mask_name)):
                print("path {}/{} not exist !".format(mask_path, mask_name))
                continue

            # print(mask[mask != 0])
            # exit()
            print(mask[mask!=0])
            mask[mask!=255] = 0
            mask[mask==255] = 1
            mask_jud = (mask == 1).__contains__(1)
            # print(mask_jud)
            if mask_jud is False:
                no_aim_num += 1
                print("no_aim_num:", no_aim_num)
                continue

            # mask[mask != label] = 0               # label  GREEN
            # mask[mask == label] = 1
            # print(mask)

            # img = cv2.blur(img, (3, 3))
            mask = mask.astype(np.uint8)
            # cv2.imwrite("{}/{}.png".format(mask_save_path, img_name), mask)
            # cv2.imwrite("{}/{}.png".format(img_save_path, img_name), img)

            img = img[:, :, ::-1]

            np.save("{}/{}_{}".format(npy_mask_save_path, name, mask_name.split(".")[0] + "_mask"), mask)
            np.save("{}/{}_{}".format(npy_img_save_path, name, mask_name.split(".")[0]), img)

            #np.save("{}/{}".format(save_path, mask_name.split(".")[0] + "_mask"), mask)
        num += 1
    print("this datasets have {} pic no aim  !".format(no_aim_num))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mask_path', type=str, default="/mnt/data1/zc_data/map_data/tianditu_data/mask", help='images dir')
    parser.add_argument('--img_path', type=str, default="/mnt/data1/zc_data/map_data/tianditu_data/img", help='coco type dataset save dir')
    # parser.add_argument('--mask_save_path', type=str, default="/mnt/data1/dzy_data/roof_segmentation_data/WHU_dataset/whu_dataset_blur/arg_data/train/masks",
    #                     help='images dir')
    # parser.add_argument('--img_save_path', type=str, default="F:/datasets/map_datasets/WHU_dataset/new_images",
    #                     help='coco type dataset save dir')
    parser.add_argument('--npy_img_save_path', type=str, default="/mnt/data1/zc_data/map_data/tianditu_data/images",
                        help='coco type dataset save dir')
    parser.add_argument('--npy_mask_save_path', type=str, default="/mnt/data1/zc_data/map_data/tianditu_data/masks",
                        help='coco type dataset save dir')

    parser.add_argument('--label', type=int, default=1, help='mask`s label_t')
    parser.add_argument('--name', type=str, default="anhui", help='mask`s label_t')

    args = parser.parse_args()


    mask_path = args.mask_path
    img_path = args.img_path
    # mask_save_path = args.mask_save_path
    # img_save_path = args.img_save_path
    npy_img_save_path = args.npy_img_save_path
    npy_mask_save_path = args.npy_mask_save_path
    name = args.name
    label = args.label

    # for cls in li:
    #     if cls != "train":
    #         mask_path = mask_path.replace("train", cls)
    #         img_path = img_path.replace("train", cls)
    #         npy_img_save_path = npy_img_save_path.replace("train", cls)
    #         npy_mask_save_path = npy_mask_save_path.replace("train", cls)
    convert_mask(mask_path,  img_path,  label, npy_mask_save_path, npy_img_save_path, name)