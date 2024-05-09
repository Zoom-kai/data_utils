import os
from tqdm import tqdm
import numpy as np
import cv2

from osgeo import gdal
file_path = "/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/suzhou_shitang"
png_path = "/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/suzhou_shitang_png"



if not os.path.exists(png_path):
    os.makedirs(png_path)

if not os.path.exists(png_path.replace("images", "masks")):
    os.makedirs(png_path.replace("images", "masks"))

names = os.listdir(file_path)
n = 0
for name in tqdm(names):
    if name.split(".")[-1] != "tif":
        continue
    if n > 100:
        break
    ds=gdal.Open(os.path.join(file_path, name))
    data = ds.ReadAsArray()

    # print(data)
    # ds = np.array(ds)
    # print(ds)
    data = np.transpose(data, [1, 2, 0])
    print(data.shape)
    cv2.imwrite(os.path.join(png_path, name.replace("tif", "png")), data)

    # cv2.imwrite(os.path.join(png_path, name.replace("tif", "png")), data)


    # mask_path = os.path.join(file_path.replace("images", "masks"), name)
    # mask_save_path = os.path.join(png_path.replace("images", "masks"), name.replace("tif", "png"))
    #
    # ds=gdal.Open(mask_path)
    # data1 = ds.ReadAsArray()
    #
    # # data1 = np.transpose(data1, [1, 2, 0])
    # cv2.imwrite(mask_save_path, data1)