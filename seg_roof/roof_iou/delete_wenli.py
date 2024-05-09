import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import ndimage
from contours import figure_num

cov_len = 23  # 尽量选取比较大的卷积核
img = Image.open("57_shanghai1_213.png", 'r')
img = img.convert('L')
avg_img = []
for i in range(19):  # 循环次数不限，尽量不要太多
    px = np.random.randint(0, 256 - cov_len)
    py = np.random.randint(0, 256 - cov_len)
    rect = (px, py, px + cov_len, py + cov_len)
    cut_img = img.crop(rect)
    print(np.array(cut_img).shape)
    avg_img.append(np.array(cut_img).reshape(-1))
avg_img = np.array(avg_img).mean(axis=0).reshape(cov_len, cov_len)

avg_img = avg_img / avg_img.sum()  # 加权平均

i = ndimage.convolve(img, avg_img)      # 多维卷积， 权重数组，与输入的维数相同
print(i)

k, contours = figure_num(i)

print(k)
img_result = Image.fromarray(i)
img_result.save('wenli_out/6.png')
plt.imshow(img_result, cmap='gray')
plt.show()