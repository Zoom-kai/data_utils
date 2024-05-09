
import cv2
import numpy as np




# 求两个ROI的交并补等操作
def or_and_not_xor_main():
    #1， 创建第一个image与mask
    img_zero = np.zeros((900, 1200, 3), dtype=np.uint8)
    img_zero_sample = img_zero.copy()
    img_zero_2 = img_zero.copy()
    print(img_zero.shape)

    # points = np.array([[101, 101], [110, 101], [101, 110], [110, 110]])
    # points_ROI = np.array([[101, 101], [110, 101], [110, 110], [101, 110]])
    points_ROI = np.array([[101, 101], [300, 101], [300, 300], [101, 300]])
    # 画顶点
    # for i in range(len(points)):
    #     cv2.circle(img_zero, tuple(points[i]), 5, (0,255,255), -1)

    # 填充mask
    # cv2.fillPoly(img_zero, [points], (0, 0, 255))  # 任意多边形
    cv2.fillConvexPoly(img_zero, points_ROI, (255, 255, 255))  # 凸包
    img_gray_roi_mask = cv2.cvtColor(img_zero, cv2.COLOR_RGB2GRAY)

    # img_gray_roi_mask中mask的面积，即为白色的点
    mask = img_gray_roi_mask[img_gray_roi_mask > 0]
    print(len(mask)) # 100个点

    # cv2.imshow('img_gray_roi_mask A', img_gray_roi_mask)

    #2, 创建第二个image与mask
    points_ROI_triangle = np.array([[201, 100], [400, 100], [300, 300]])
    # 填充mask
    cv2.fillConvexPoly(img_zero_2, points_ROI_triangle, (0, 255, 255))  # 凸包
    img_gray_roi_mask_triangle = cv2.cvtColor(img_zero_2, cv2.COLOR_RGB2GRAY)
    #灰度化后的图转化为白色255
    img_gray_roi_mask_triangle[img_gray_roi_mask_triangle > 0] = 255
    # cv2.imshow('img_gray_roi_mask_triangle B', img_gray_roi_mask_triangle)


    print(img_gray_roi_mask.shape, img_gray_roi_mask_triangle.shape)
    #3.1， 求 img_gray_roi_mask(named: A) 与 img_gray_roi_mask_triangle(named: B) 的并集
    A_or_B = cv2.bitwise_or(img_gray_roi_mask, img_gray_roi_mask_triangle)
    # cv2.imshow('A_or_B', A_or_B)

    #3.2， 求 img_gray_roi_mask(named: A) 与 img_gray_roi_mask_triangle(named: B) 的交集
    A_and_B = cv2.bitwise_and(img_gray_roi_mask, img_gray_roi_mask_triangle)
    # cv2.imshow('A_and_B', A_and_B)

    # 3.3， 求属于A，但不属于B的部分：A-AB
    A_sub_AB = cv2.bitwise_xor(img_gray_roi_mask, A_and_B)
    # cv2.imshow('A_sub_AB', A_sub_AB)

    # 3.4， 求A与B的并集关于整张图片的补集，即求整张图片扣去A和B
    A_or_B_not = cv2.bitwise_not(A_or_B)
    # cv2.imshow('A_or_B_not', A_or_B_not)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


or_and_not_xor_main()