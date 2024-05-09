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
    address = addr + str(num) + '.png'
    cv2.imwrite(address, image)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, default=r"/mnt/data1/zc_code/yolov5-6.0/data/dataset/shuibei_0310/video/IP Positioning System20230308155110 .mp4", help='images dir')

    parser.add_argument('--img_save_path', type=str, default=r"/mnt/data1/zc_code/yolov5-6.0/data/dataset/shuibei_0310/video/shuibei_51101/" , help='coco type dataset save dir')
    args = parser.parse_args()
    video_path = args.video_path
    img_save_path = args.img_save_path
    # 读取视频文件
    videoCapture = cv2.VideoCapture(video_path)

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
            if i > 3000:
                break
            if i%3 == 0:
                if success:
                    print('save image:', i)
                    print(frame.shape)
                    save_image(frame, img_save_path, i)

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