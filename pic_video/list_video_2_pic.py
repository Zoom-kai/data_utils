# 导入所需要的库
import cv2
import numpy as np
import os
import argparse
# 定义保存图片函数
# image:要保存的图片名字
# addr；图片地址与相片名字的前部分
# num: 相片，名字的后缀。int 类型
def save_image(image, addr, num):
    address = os.path.join(addr, str(num) + '.png')
    cv2.imwrite(address, image)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, default=r"D:\BaiduNetdiskDownload\0703_yiranwu\trim_0703", help='images dir')

    parser.add_argument('--img_save_dir', type=str, default=r"D:\BaiduNetdiskDownload\0703_yiranwu\trim_0703_pic", help='coco type dataset save dir')
    args = parser.parse_args()
    video_path = args.video_path
    img_save_dir = args.img_save_dir

    # 读取视频文件
    vid_list = os.listdir(video_path)
    for name in vid_list:

        vid_path = os.path.join(video_path, name)

        videoCapture = cv2.VideoCapture(vid_path)

        img_save_path = os.path.join(img_save_dir, name)

        if not os.path.exists(img_save_path):
            os.makedirs(img_save_path)


        fps = videoCapture.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        # 读帧
        i = 0
        while True:
            if videoCapture.grab():
                success, frame = videoCapture.read()
                print(success)
                i = i + 1
                if i % 25 == 0:
                    if success:
                        print('save image:', i)
                        print(frame.shape)
                        print(img_save_path,"{}_{}.jpg".format(name.split(".")[0], i))
                        save_image(frame, img_save_path, "{}_{}".format(name.split(".")[0], i))

                else:
                    continue
            else:
                break


    # i = 0
    # while i <= 1500:
    #     try:
    #         success, frame = videoCapture.read()
    #         print(success)
    #         i = i + 1
    #         if success:
    #             print('save image:', i)
    #             save_image(frame, img_save_path, i)
    #     except ValueError as value_err:
    #         print(value_err)
    #         continue