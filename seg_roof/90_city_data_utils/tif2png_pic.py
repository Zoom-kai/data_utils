import os
from tqdm import tqdm
import numpy as np
import cv2

from osgeo import gdal
file_path = "/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/suzhou_tif"
png_path = "/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/suzhou_png"



if not os.path.exists(png_path):
    os.makedirs(png_path)
names = os.listdir(file_path)
n = 0
for name in tqdm(names):
    # if n > 100:
    #     break
    print(os.path.join(file_path, name))
    ds=gdal.Open(os.path.join(file_path, name))
    data = ds.ReadAsArray()

    # print(data)
    # ds = np.array(ds)
    # print(ds)
    # data[data!=0] = 1
    # print(data[data!=0])

    print(data.shape)
    data = np.transpose(data, [1, 2, 0])
    # print(data.shape)
    # data =  cv2.cvtColor(data, cv2.COLOR_RGB2GRAY)
    # print(data.shape)
    cv2.imwrite(os.path.join(png_path, name.replace("tif", "png")), data)

