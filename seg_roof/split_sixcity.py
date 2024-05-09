import os
from tqdm import tqdm
import cv2
import numpy as np
import cv2
from tqdm import tqdm
import numpy
import math
import string
import os
import argparse
import numpy as np
import json

def split(
    img,    #image matrix
    ratio_x,  #patch_length/image_length
    ratio_y,
    n_x,      #number of patches per line
    n_y,
    dstPath, #destination path,
    img_name
         ):
    height = img.shape[0]
    width = img.shape[1]
    #cv2.imshow(imgPath, img)
    pWidth = int(ratio_x * width)
    pWidthInterval = 0
    pHeight = int(ratio_y * height)
    pHeightInterval = 0
    if n_y == 1:
        pHeight = int(ratio_y * height)
        pHeightInterval = 0
    else:
        pHeight = int(ratio_y*height)
        pHeightInterval = (height-pHeight)/(n_y-1)

    if n_x == 1:
        pWidth = int(ratio_x * width)
        pWidthInterval = 0
    else:
        pWidth = int(ratio_x*width)
        pWidthInterval = int((width-pWidth)/(n_x-1))
    cnt = 1

    for i in range(n_x):
        for j in range(n_y):
            x = int(pWidthInterval * i)
            y = int(pHeightInterval * j)

            if len(img.shape) == 3:
                patch = img[y:y+pHeight, x:x+pWidth, :]
                patch = cv2.blur(patch, (4, 4))
                cv2.imwrite('{}/{}_{}.png'.format(dstPath, img_name, cnt), patch)

                # patch = patch[:, :, ::-1]

                cnt += 1


            else:
                patch = img[y:y+pHeight, x:x+pWidth]
                cv2.imwrite('{}/{}_{}.png'.format(dstPath, img_name, cnt), patch)
                cnt += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mask_path', type=str, default="/mnt/data1/zc_code/tmp/dataset_utils/gudewei/tiandi_mask/mask_o", help='images dir')
    parser.add_argument('--img_path', type=str, default="/mnt/data1/zc_code/tmp/dataset_utils/gudewei/tiandi_mask/img_o", help='coco type dataset save dir')
    parser.add_argument('--mask_save_path', type=str, default="/mnt/data1/zc_code/tmp/dataset_utils/gudewei/tiandi_mask/mask",
                        help='images dir')
    parser.add_argument('--img_save_path', type=str, default="/mnt/data1/zc_code/tmp/dataset_utils/gudewei/tiandi_mask/img",
                        help='coco type dataset save dir')
    args = parser.parse_args()

    # img_path = r"/mnt/data1/dzy_data/building_segmentation_data/SixCityDataset/zurich"
    # save_mask_path = r"/mnt/data1/dzy_data/building_segmentation_data/SixCityDataset/split_data/zurich/label"
    # save_img_path = r"/mnt/data1/dzy_data/building_segmentation_data/SixCityDataset/split_data/zurich/image"

    mask_path = args.mask_path
    img_path = args.img_path
    save_mask_path = args.mask_save_path
    save_img_path = args.img_save_path


    if os.path.exists(save_img_path) == False:
        os.makedirs(save_img_path)

    if os.path.exists(save_mask_path) == False:
        os.makedirs(save_mask_path)

    img_list = os.listdir(img_path)
    for img_name in tqdm(img_list):
        # print(img_name)
        # print(img_name.split(".")[0][-5:])
        # exit()
        # if img_name.split(".")[0][-5:] != "image":
        #     continue
        mask_name = img_name
        # print(mask_name)
        img = cv2.imread("{}/{}".format(img_path, img_name))
        mask = cv2.imread("{}/{}".format(mask_path, mask_name), cv2.IMREAD_GRAYSCALE)
        if mask is None:
            print(None)
            continue

        h, w, c = img.shape
        # mask = mask[:, :, 0]                # r ??
        # print(mask)

        # mask[mask == 0] = 1
        # mask[mask == 255] = 0
        # print(mask[mask==[0, 0, 255]])

        # reshape_h = int(img.shape[0]/3)
        # reshape_w = int(img.shape[1]/3)
        # print(reshape_w, reshape_h)

        mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_LINEAR)

        pad_h = int((512 - (img.shape[0])%512))
        top = int(pad_h/2)
        bottom = pad_h-top
        pad_w = int((512 - (img.shape[1])%512))
        right = int(pad_w/2)
        left = pad_w - right

        # print(pad_h, pad_w)
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0))
        mask = cv2.copyMakeBorder(mask, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0))
        # print(img.shape[0], img.shape[1])


        # img[mask == 1, 2] = 255

        # print(img.shape, mask.shape)

        raito_y = 512/img.shape[0]
        ratio_x = 512/img.shape[1]
        n_x = int(img.shape[0]/512)
        n_y = int(img.shape[1]/512)
        img_name = img_name.split(".")[0]
        split(img, ratio_x, raito_y, n_x, n_y, save_img_path, img_name)
        split(mask, ratio_x, raito_y, n_x, n_y, save_mask_path, img_name)

        # exit()



