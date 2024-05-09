import cv2
import os
import argparse
from tqdm import tqdm

def get_file_names(search_path):
    for (dirpath, _, filenames) in os.walk(search_path):
        for filename in filenames:
            yield filename  # os.path.join(dirpath, filename)

def save_to_video(imgpath, output_video_file, frame_rate):
    # list_files = sorted([int(i.split('_')[-1].split('.')[0]) for i in get_file_names(imgpath)])
    # 拿一张图片确认宽高
    img_list = os.listdir(imgpath)
    # print(img_list)
    # img_list.sort(key=lambda x:int(x.split(".")[0]))
    img_list.sort(key=lambda x:int(x.split(".")[0].split('_')[-1]))
    print(img_list)
    # exit()
    img0 = cv2.imread("{}/{}".format(imgpath, img_list[0]))
    # img0 = cv2.resize(img0, (360, 640))
    # print(img0)
    #img0 = cv2.imread(os.path.join(imgpath, '%s.jpg' % list_files[0]))
    # print(img0)
    height, width, layers = img0.shape
    print(img0.shape)
    # 视频保存初始化 VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videowriter = cv2.VideoWriter(output_video_file, fourcc, frame_rate, (width, height))
    # 核心，保存的东西
    with tqdm(total=len(img_list)) as pbar:
        for f in img_list:
            # print("saving..." + f)
            img = cv2.imread("{}/{}".format(imgpath, f))
            # img = cv2.resize(img, (360, 640))

            videowriter.write(img)
            pbar.update(1)
    videowriter.release()
    cv2.destroyAllWindows()
    print('Success save %s!' % output_video_file)
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgpath', type=str, default=r"/mnt/data1/zc_code/yolov5-6.0/runs/detect/shuibei_14/", help='xml files dir')
    parser.add_argument('--videopath', type=str, default=r"/mnt/data1/zc_code/yolov5-6.0/data/dataset/shuibei_0310/video/shuibei_14.mp4", help='coco type dataset save dir')
    args = parser.parse_args()

    imgpath = args.imgpath                          # 输入图片存放位置
    output_video_file= args.videopath              # 输入视频保存位置以及视频名称

    # 图片变视频

    save_to_video(imgpath, output_video_file, 20)
