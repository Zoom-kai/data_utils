import cv2
import numpy as np
import os
import gdal
import random


def contrast_brightness_demo(image, c, b):
    h, w, channels = image.shape
    blank = np.zeros([h, w, channels], image.dtype)
    dst = cv2.addWeighted(image, c, blank, 1 - c, b)
    cv2.imshow('demo_image', dst)
    cv2.waitKey(0)
    return dst

tiff_file = "E:\code\map_utils\spacenet\RGB-PanSharpen_AOI_3_Paris_img75.tif"
# tiff_file = "F:\code\map_utils\spacenet\RGB-PanSharpen_AOI_3_Paris_img3.tif"
dataset = gdal.Open(tiff_file)
# num_channels = dataset.RasterCount
#
band1 = dataset.GetRasterBand(1)  # Red channel
band2 = dataset.GetRasterBand(2)  # Green channel
band3 = dataset.GetRasterBand(3)  # Blue channel

b1 = band1.ReadAsArray()
b2 = band2.ReadAsArray()
b3 = band3.ReadAsArray()

img_np = np.dstack((b3, b2, b1))
# img_np = np.dstack((b1, b2, b3))
print("img_np.max():{}".format(img_np.max()))
img_np = (img_np/img_np.max())
# img_np = (img_np/2048.0)

cv2.imshow("origin", img_np)
print(img_np)

# gamma = random.uniform(0.4, 1.6)
img_gamma = np.power(img_np, 0.6)
cv2.imshow("img_gamma", img_gamma)


img = (img_gamma * 255).astype(np.uint8)

img = contrast_brightness_demo(img, 0.7, 80)

# image = (img_np *1).astype(np.uint8)
# tiff = georaster.MultiBandRaster(tiff_file)
# image = tiff.r / 2048.0



cv2.imshow("img", img)
cv2.waitKey(0)


print(img)
cv2.imwrite("RGB-PanSharpen_AOI_3_Paris_img7511223.png", img)

