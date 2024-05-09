from geojson_to_array import *
from plot_coords import *
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal

if __name__ == '__main__':
    print("begin !")
    # raster_file = "/home/pang/zc/seg/spacenet/sn2_AOI_4_Shanghai/RGB-PanSharpen/RGB-PanSharpen_AOI_4_Shanghai_img99.tif"
    # geojson_file = "/home/pang/zc/seg/spacenet/sn2_AOI_4_Shanghai/geojson/buildings/buildings_AOI_4_Shanghai_img99.geojson"

    raster_file = "/home/pang/zc/seg/spacenet/sn2_AOI_3_Paris/RGB-PanSharpen/RGB-PanSharpen_AOI_3_Paris_img37.tif"
    geojson_file = "/home/pang/zc/seg/spacenet/sn2_AOI_3_Paris/geojson/buildings/buildings_AOI_3_Paris_img37.geojson"

    save_path = "/mnt/data1/zc_data/geo_pic"
    pixel_arr = geojson_to_pixel_arr(raster_file, geojson_file)
    print(pixel_arr)
    print(3333333333333)
    # fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(16, 16))
    pixel_arr = np.array(pixel_arr)
    print(pixel_arr.shape)

    dataset = gdal.Open(raster_file)
    num_channels = dataset.RasterCount

    band1 = dataset.GetRasterBand(1)  # Red channel
    band2 = dataset.GetRasterBand(2)  # Green channel
    band3 = dataset.GetRasterBand(3)  # Blue channel

    b1 = band1.ReadAsArray()
    b2 = band2.ReadAsArray()
    b3 = band3.ReadAsArray()

    img_np = np.dstack((b3, b2, b1))
    # print("777777777777", img_np)

    plot_img = plot_truth_coords(img_np, pixel_arr)