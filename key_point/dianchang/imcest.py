import cv2
import matplotlib.pyplot as plt



img = cv2.imread("save_roof11.jpg", cv2.IMREAD_GRAYSCALE)
print(img[img!=0])
plt.imshow(img)
plt.show()
