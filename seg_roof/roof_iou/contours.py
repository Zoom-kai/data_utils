import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import torch
from scipy import ndimage


def figure_num(img):
    # print(img)
    t0 = time.time()
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # print(img.shape)
    blur_dst=cv2.GaussianBlur(img,(3,3),0)
    # blur_dst = delete_wenli(blur_dst)       # 去除细节纹理

    #OTSU阈值分割
    ret,otsu_dst=cv2.threshold(blur_dst,0,255,cv2.THRESH_OTSU)
    # cv2.imshow("s", otsu_dst)
    #Canny算子提取边缘轮廓
    canny_dst=cv2.Canny(otsu_dst,10,250)

    canny_dst[canny_dst>0] = 1
    img[img>0] = 1

    v = (canny_dst[canny_dst>0].sum())/(img[img>0].sum())

    # print(img.shape[0]*img.shape[1])
    print("v:", v)
    # print(canny_dst[canny_dst!=0])
    # print(canny_dst.max(), canny_dst.min())


    # cv2.imshow("s", canny_dst)
    # plt.imshow(canny_dst)
    # plt.show()

    #寻找二值图像轮廓点
    # edge_points,h=cv2.findContours(canny_dst,cv2.RETR_EXTERNAL,
    #                             cv2.CHAIN_APPROX_SIMPLE)
    # contours=edge_points
    # #轮廓的数量
    # k=len(edge_points)
    # print(2222222222222, edge_points, k)
    t1 = time.time()

    # print('time:{}'.format(t1 - t0))
    return v

def delete_wenli(gray):
    avg_img = []
    cov_len = 23  # 尽量选取比较大的卷积核
    for i in range(19):  # 循环次数不限，尽量不要太多
        px = np.random.randint(0, 128 - cov_len)
        py = np.random.randint(0, 128 - cov_len)
        rect = (px, py, px + cov_len, py + cov_len)
        # print(rect)
        # cut_img = img.crop(rect)
        py2 = py+cov_len
        px2 = px+cov_len
        # print(px, py, px2, py2)
        cut_img = gray[py:py2, px:px2]

        avg_img.append(np.array(cut_img).reshape(-1))

        # print(np.array(cut_img).reshape(-1).shape)
        # print(np.array(avg_img).shape, np.array(avg_img).mean(axis=0).shape)
    avg_img = np.array(avg_img).mean(axis=0).reshape(cov_len, cov_len)

    avg_img = avg_img / avg_img.sum()  # 加权平均

    i = ndimage.convolve(gray, avg_img)  # 多维卷积，权重数组，与输入的维数相同

    return i

def draw_test():
    import cv2
    import numpy as np

    rows = 512
    cols = 512

    # Create image with new colour for replacement
    img = np.zeros((rows, cols, 3), np.uint8)
    img[:, :] = (0, 0, 0)

    # img=cv2.copyMakeBorder(img,1,1,1,1, cv2.BORDER_CONSTANT, value=[0,0,0])

    # Draw rectangle
    img = cv2.rectangle(img, (400, 0), (512, 100), (255, 255, 255), -1)
    img = cv2.rectangle(img, (0, 400), (300, 100), (255, 255, 255), -1)

    plt.imshow(img)
    plt.show()
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find Contour
    # contours, hierarchy = cv2.findContours(imggray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(img, contours, 0, (0, 0, 255), -1)

    plt.imshow(img)
    plt.show()
    return print(1111111111111)



if __name__=="__main__":
    # draw_test()
    import os
    # exit()
    img_path = "roof_input"
    img_list = os.listdir(img_path)
    for name in img_list:
        print(name)
        img=cv2.imread("{}/{}".format(img_path, name))
        # print(img.shape)
        #img1=cv2.imread("D:/testimage/sample.jpg")
        #灰度化+高斯滤波

        t0 = time.time()
        #轮廓的数量
        # k, contours=figure_num(img)
        v=figure_num(img)
        print(v)

        continue
        exit()
        # for pic in contours:
        #     plt.imshow(pic)
        #     plt.show()
        # exit()
        src=np.zeros((img.shape[0], img.shape[1]),np.uint8)
        src1=np.zeros((img.shape[0], img.shape[1]),np.uint8)
        h, w, c = img.shape
        print(img.shape)
        contours1 = []
        p = []
        p3 = []
        p2 = []
        for i in range(k):

            #画出轮廓
            # cv2.drawContours(src,contours,i,250, 1)
            # plt.imshow(contours[i])
            # plt.show()
            for point in contours[i]:

                # if point[0][0] == 0 and point[0][1] != 0:
                if 0  in point[0] or h-1 in point[0] or w-1 in point[0]:
                    print(point[0])
                    p.append(point[0])
                    print("pppppppp: ", p)
                else:
                    p2.append(point)
            print("len(p): {}".format(len(p)))


            if p != []:
                if p[0][0] != p[1][0] and p[0][1] != p[1][1]:
                    if p[0][0] == p[1][1]:
                        cv2.line(src, (p[0][0], p[0][1]), (p[0][0], p[0][0]), 255, 1)
                        cv2.line(src, (p[1][0], p[1][1]), (p[0][0], p[0][0]), 255, 1)
                        p3 = [[p[0][0], p[1][0]]]

                    elif p[0][1] == p[1][0]:
                        cv2.line(src, (p[0][0], p[0][1]), (p[0][1], p[0][1]), 255, 1)
                        cv2.line(src, (p[1][0], p[1][1]), (p[0][1], p[0][1]), 255, 1)
                        p3 = [[p[0][1], p[1][0]]]
                else:
                    cv2.line(src, (p[0][0], p[0][1]), (p[1][0], p[1][1]), 255, 1)
                    p3 = [[int((p[0][0]+p[1][0])/2), int((p[0][1]+p[1][1])/2)]]
                print(contours[i].shape)
                c = np.append(contours[i], p3).reshape(-1, 1, 2)
                print(c)
                print(c.shape)
                # exit()
                contours1.append(c)
            # cv2.drawContours(src, contours, i, 255, cv2.FILLED)

        contours1 = contours1 + p2
        print(len(contours))
        print(len(contours1))

        for n in range(len(contours1)):
            cv2.drawContours(src, contours1, n, 255, -1)

            # cv2.drawContours(src,src,i,255,1)

        # k2, contours = figure_num(src)
        # print(k2)
        # print(k)
        # exit()
            # #最小外包圆
            # circle=cv2.minEnclosingCircle(contours[i])
            # # circle = cv2.minEnclosingTriangle(contours[i])
            # cv2.circle(img,(int(circle[0][0]),int(circle[0][1])),int(circle[1]),(0,255,0),2)
            # #绘制多边形
            # approxCurve=cv2.approxPolyDP(contours[i],0.3,True)
            # t=approxCurve.shape[0]
            # for i in range(t-1):
            #     cv2.line(img,(approxCurve[i,0,0],approxCurve[i,0,1]),
            #             (approxCurve[i+1,0,0],approxCurve[i+1,0,1]),(255,0,0),2)
            #     cv2.line(img, (approxCurve[t-1, 0, 0], approxCurve[t-1, 0, 1]),
            #             (approxCurve[0, 0, 0], approxCurve[0, 0, 1]),(255,0,0),2)
        # cv2.imshow("1",src)
        # cv2.imshow("2",img)

        t1 = time.time()
        print("1111111111111  fill contours need time : {} s".format(t1-t0))
        # cv2.drawContours(src, src, 0, 250, -1)

        cv2.imwrite("output_mask/result-1.jpg", src)
        cv2.imwrite("output_mask/result-2.jpg", img)
        # print(111111111111)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

