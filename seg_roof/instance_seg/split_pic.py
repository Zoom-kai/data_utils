import cv2
import os
import matplotlib.pyplot as plt

pic_path = "./input/"
save_path = "output"


pic_list = os.listdir(pic_path)


for name in pic_list:
    img_ori = cv2.imread("{}/{}".format(pic_path, name))
    h, w = img_ori.shape[0], img_ori.shape[1]

    img_new = img_ori[int(h*0.12):h, int(w*0.12): w]

    # img_new = img_new[..., ::-1]
    # plt.imshow(img_new)
    # plt.show()
    # exit()
    cv2.imwrite("{}/{}".format(save_path, name), img_new)