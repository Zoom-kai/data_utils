import cv2
from PIL import Image
import numpy as np
# from osgeo import gdal
import tifffile as tif

ds = tif.imread("./MUL_AOI_3_Paris_img19.tif")
print(ds)
img_np = np.array(ds)

img = img_np[:, :, 0:3]  #[..., ::-1]

img = (img/img.max())*255
print(img.shape)

cv2.imwrite("test_tif_img.jpg", img)
# cv2.imshow('cartoon window', img_np)
# # 等待用户按下任意键
# cv2.waitKey(0)
# # 释放内存
# cv2.destroyAllWindows()
#
#
# exit()
# img = Image.open("/mnt/data1/zc_code/tmp/dataset_utils/AOI/MUL_AOI_3_Paris_img19.tif")
# RGBIMG = img.convert("RGB")
# img_np = np.array(RGBIMG)
# print(img_np)
#
exit()
# img = cv2.imread("MUL_AOI_3_Paris_img19.tif")
print(img)
# 传入所要展示的图片
# cv2.imshow('cartoon window', img)
# 等待用户按下任意键
# cv2.waitKey(0)
# 释放内存
cv2.destroyAllWindows()