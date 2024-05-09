from PIL import Image
import os
from tqdm import tqdm

path = r"/mnt/data1/zc_data/map_data/china_90_city_datasets/Simplified_Version_1/Tier2/Shenzhen/dataset/masks_tif"
tif_list = os.listdir(path)
save_path = r"/mnt/data1/zc_data/map_data/china_90_city_datasets/Simplified_Version_1/Tier2/Shenzhen/dataset/masks_png"
for tif in tif_list:
    tif_name = os.path.splitext(tif)[0]
    print(tif_name)
    tif_path = os.path.join(path, tif)
    # cprealDir = os.path.join(save_path, tif_name)
    # if os.path.exists(cprealDir):
    #     pass
    # else:
    #     os.makedirs(cprealDir)
    img = Image.open(tif_path)
    # print(len(img.seek()))
    # print(img)
    for i in range(100):
        try:
            img.seek(i)
            img.save(os.path.join(save_path, tif_name + '.png'))
        except EOFError:
            break


