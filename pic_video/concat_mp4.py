from moviepy.editor import *
import os
from tqdm import tqdm

L = []

# Python视频片段存放的文件夹
for root, dirs, files in os.walk(r"D:\datasets\peidianfang\peidianfang_20220104\video\hebinshipin"):
    files.sort()  # 按文件名排序
    print(files)
    for file in tqdm(files):  # 遍历所有文件

        if os.path.splitext(file)[1] == '.mp4':  # 筛选后缀名为.mp4的视频文件
            filePath = os.path.join(root, file)  # 拼接完整文件路径
            video = VideoFileClip(filePath)  # 载入视频
            L.append(video)  # 添加到数组
    final_clip = concatenate_videoclips(L)
    final_clip.to_videofile(r"D:\datasets\peidianfang\peidianfang_20220104\video\hebinshipin\hebing.mp4", fps=25, remove_temp=False)


