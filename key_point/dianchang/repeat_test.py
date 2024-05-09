import numpy as np

t = np.arange(0, 27)

print(t)

out = t[..., None]

print(out)

# 为啥脚手架代码里会出现 2 ？？
out1 = out.repeat(1, 2)

print(out1)