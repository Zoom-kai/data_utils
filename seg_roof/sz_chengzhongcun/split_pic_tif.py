import cv2
import os
import cv2
from PIL import Image
import numpy as np
# from osgeo import gdal
import tifffile as tif

# ds = tif.imread("/mnt/data1/zc_data/sz_map/build_pic/masks/sz_img_23_101.tif")
# # print(ds)
# img_np = np.array(ds)
# print(img_np)
# print(img_np[img_np!=0])
# img = img_np[:, :, 0:]  #[..., ::-1]
# img = (img/img.max())*255
# print(img)


from osgeo import gdal
# import numpy as np
gtif = gdal.Open("/mnt/data1/zc_data/sz_map/sz_img.tif")
band = gtif.GetRasterBand(1)
bandArray = band.ReadAsArray()
print(bandArray)
print(bandArray[bandArray!=0])
print(np.max(bandArray))


