import io
from PIL import Image
import os
import shutil
from shutil import copy2
from tqdm import tqdm

def is_dark(img_path, darkness_threshold=40):
    with open(img_path, 'rb') as f:
        img_data = io.BytesIO(f.read())
    im = Image.open(img_data)
    luma = im.convert('L').histogram()
    darkness = sum(luma[:darkness_threshold])
    total = sum(luma)
    ratio = darkness / total
    return ratio > 0.5
def delete_dark_images(folder_path, darkness_pic_path):
    for root, dirs, files in os.walk(folder_path):
        for file in tqdm(files):
            file_path = os.path.join(root, file)
            if is_dark(file_path):
                # os.remove(file_path)
                shutil.move(file_path, darkness_pic_path)
                # copy2(file_path, darkness_pic_path)
folder_path = r'/mnt/data1/zc_data/smoke_data/classify_dataset/green_net/val/green_net'
# folder_path = '/mnt/data1/zc_data/smoke_data/classify_dataset/green_net_dk'
darkness_pic_path = r'/mnt/data1/zc_data/smoke_data/classify_dataset/darkness_green_net'
if not os.path.exists(darkness_pic_path):
    os.makedirs(darkness_pic_path)

delete_dark_images(folder_path, darkness_pic_path)