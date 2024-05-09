from geojson_to_array import *
from plot_coords import *
import os
import cv2
from PIL import Image





if __name__ == '__main__':
    print("begin !")
    tif_path = "/mnt/data1/dzy_data/remote_sensing_data/AOI_3_Paris_Train/RGB-PanSharpen"
    geojson_path = "/mnt/data1/dzy_data/remote_sensing_data/AOI_3_Paris_Train/geojson/buildings"
    save_path = "/mnt/data1/zc_data/geo_pic/paris"

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    tif_list = os.listdir(tif_path)
    n = 0
    for tif_name in tif_list:

        raster_file = "{}/{}".format(tif_path, tif_name)
        geojson_file = "{}/buildings{}".format(geojson_path, tif_name.replace("tif", "geojson")[14:])
        pixel_arr = geojson_to_pixel_arr(raster_file, geojson_file)

        pixel_arr = np.array(pixel_arr)
        print("len(pixel_arr):", len(pixel_arr))
        #if pixel_arr is None:
        if not len(pixel_arr) > 0:
            print("11111111111111111, NONE")
            continue
        n += 1
        print("n:{}".format(n))
        dataset = gdal.Open(raster_file)
        num_channels = dataset.RasterCount

        band1 = dataset.GetRasterBand(1)  # Red channel
        band2 = dataset.GetRasterBand(2)  # Green channel
        band3 = dataset.GetRasterBand(3)  # Blue channel

        b1 = band1.ReadAsArray()
        b2 = band2.ReadAsArray()
        b3 = band3.ReadAsArray()

        img_np = np.dstack((b1, b2, b3))

        img_np = img_np/img_np.max()
        
        im = Image.fromarray(img_np.astype(np.uint8))  
        #im = Image.fromarray(img_np.astype(np.uint8))  
        im.save("{}/{}".format(save_path, tif_name))



        #plot_img = plot_truth_coords(img_np, pixel_arr, save_path, plot_name=tif_name)



    # raster_file = "/home/pang/zc/seg/spacenet/sn2_AOI_4_Shanghai/RGB-PanSharpen/RGB-PanSharpen_AOI_4_Shanghai_img99.tif"
    # geojson_file = "/home/pang/zc/seg/spacenet/sn2_AOI_4_Shanghai/geojson/buildings/buildings_AOI_4_Shanghai_img99.geojson"
    # pixel_arr = geojson_to_pixel_arr(raster_file, geojson_file)
    # print(pixel_arr)
    #
    # plot_img = plot_truth_coords(raster_file, pixel_arr)
