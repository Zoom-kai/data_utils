import os
import cv2



img_path = "/mnt/data1/zc_data/map_data/tianditu_data/img_ori"
old_model_out = "/mnt/data1/zc_data/map_data/tianditu_data/output_old_model"
tianditu_mask_path = "/mnt/data1/zc_data/map_data/tianditu_data/masks_ori"

save_path = "/mnt/data1/zc_data/map_data/tianditu_data/mask_map"
img_list = os.listdir(img_path)
for img_name in img_list:
    img = cv2.imread("{}/{}".format(img_path, img_name))
    tianditu_mask = cv2.imread("{}/{}".format(tianditu_mask_path, img_name), cv2.IMREAD_GRAYSCALE)
    out_mask = cv2.imread("{}/{}".format(old_model_out, img_name), cv2.IMREAD_GRAYSCALE)

    print(tianditu_mask[tianditu_mask!= 0], 111111111, out_mask[out_mask!= 0])
    h, w = out_mask.shape

    tianditu_mask = cv2.resize(tianditu_mask, (w, h))

    out_mask[tianditu_mask == 255] = 0
    img[out_mask == 255, :] = 0

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    cv2.imwrite("{}/{}".format(save_path, img_name), img)


