import cv2
import os
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--imgpath', type=str, default=r"best_0598",
                    help='images dir')
parser.add_argument('--newpath', type=str, default=r"best_0598_resize",
                    help='xml files dir')
args = parser.parse_args()


imgpath = args.imgpath
newpath = args.newpath
if not os.path.exists(newpath):
    os.makedirs(newpath)

img_list = os.listdir(imgpath)

for img_name in tqdm(img_list):

    img = cv2.imread("{}/{}".format(imgpath, img_name))


    img = cv2.resize(img ,(1280, 720))

    cv2.imwrite("{}/{}".format(newpath, img_name), img)
