import cv2
import os


mask = cv2.imread("/mnt/data1/zc_data/map_data/tianditu_merge/test/ningbo/ningbo_jiedaotu_masks/ningbojichang1.png",cv2.IMREAD_GRAYSCALE)
mask_shadow = cv2.imread("ningbo/ningbojichang/ningbojichang1_1.png", cv2.IMREAD_GRAYSCALE)





mask = cv2.resize(mask, (1967, 895))
mask_shadow[mask_shadow!=0] = 255

print(mask_shadow[mask_shadow!=0])
print(mask[mask!=0])
# cv2.imwrite("ningbojichang/ningbojichang_shadow.png", mask_shadow)

new_mask = mask - mask_shadow

new_mask[new_mask!=0] = 255
print(new_mask[new_mask!=0])
cv2.imwrite("ningbo/ningbojichang/ningbojichang1.png", new_mask)
