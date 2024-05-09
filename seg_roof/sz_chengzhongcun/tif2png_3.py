import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
import os
import cv2
from tqdm import tqdm

if __name__ == '__main__':
    print("begin !")

    img_path = "/mnt/data1/zc_data/sz_map/build_pic/images"
    save_path = "/mnt/data1/zc_data/sz_map/build_pic_png"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    img_list = os.listdir(img_path)
    for img_name in tqdm(img_list):
        raster_file = "{}/{}".format(img_path, img_name)

        dataset = gdal.Open(raster_file)
        num_channels = dataset.RasterCount

        # print(num_channels)
        band1 = dataset.GetRasterBand(1)  # Red channel
        band2 = dataset.GetRasterBand(2)  # Green channel
        band3 = dataset.GetRasterBand(3)  # Blue channel

        b1 = band1.ReadAsArray()
        b2 = band2.ReadAsArray()
        b3 = band3.ReadAsArray()
        img_np = np.dstack((b3, b2, b1))

        print(img_np.max())
        cv2.imwrite("{}/{}.png".format(save_path, img_name.split(".")[0]), img_np)

        # b2 = band2.ReadAsArray()
    # b3 = band3.ReadAsArray()

    # img_np = np.dstack((b3, b2, b1))
    # print(img_np[img_np!=0])

    # cv2.imwrite("test_tif2ppng.png", img_np)
