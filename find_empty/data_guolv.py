import os
from shutil import copy2
from tqdm import tqdm

cls_list = ['02010001', '02013001', '02010002', '02010006', '02010004', '02010005', '02020001', '02020003', '02020004', '02030001', '02030002', '03010001', '03010002', '03011002', '03010003', '03013001', '03020001', '03020003', '03021002', '03030001', '03030002', '03030003', '03030004', '03030006', '03030005', '03030007', '03040001', '03040002', '03040003', '03040005', '03040007', '03040008', '03040009', '03040010', '03040011', '03040012', '03040013', '03040014', '03040015', '03040016', '03040017', '03040018', '03040023', '03040024', '03040025', '03050002', '03051001', '03052001', '03060001', '03060002', '03060003', '03060004', '03063002', '04010001', '04010002', '04010004', '04020001', '04020002', '04020003', '04020004', '04020005', '05010001', '05010002', '05010003', '05010004', '06010001', '06010002', '07010001', '07010002', '07010003', '07010004', '07010005', '07010006', '07010008', '07010011', '07010012', '07010013', '07010014', '07010024', '07010032', '07020001', '07020002', '07020003', '07020004', '07030001', '07030002', '07040001', '07040002', '07040003', '07040005', '07040006']
pick_cls = ['07010002']

for cls in pick_cls:
    txt_path = r"/mnt/data1/zc_data/da_model_merge/yolo_labels"
    txt_list = os.listdir(txt_path)
    img_path = r"/mnt/data1/zc_data/da_model_merge/images/"
    new_img_path = "/mnt/data1/zc_data/da_model_merge/defect/images_{}/".format(cls)
    new_txt_path = "/mnt/data1/zc_data/da_model_merge/defect/labels_{}".format(cls)

    cls_idx = cls_list.index(cls)
    print(1111111111111111, cls_idx)
    num = 0
    if not os.path.exists(new_img_path):
        os.makedirs(new_img_path)

    if not os.path.exists(new_txt_path):
        os.makedirs(new_txt_path)

    for txt_name in tqdm(txt_list):
        if num>50:
            break
        img_name = txt_name.replace("txt", "jpg")
        a = 0
        file = open("{}/{}".format(txt_path, txt_name), "r")
        img_o = img_path + img_name
        txt_o = "{}/{}".format(txt_path, txt_name)
        try:
            for line in file.readlines():
                line = line.split(" ")
                # print(line)
                if int(line[0]) == cls_idx:
                    a = 1
            if a == 1:                          # 存在需要的类别， 就copy出去
                num += 1
                print(num)
                if not os.path.exists(img_o):
                    print("not path :{}".format(img_o))
                    continue
                copy2(img_o, new_img_path)
                copy2(txt_o, new_txt_path)
        except UnicodeDecodeError as e:
            print(e)
            print(txt_name)
            continue
    print("num add 1, sum : {}".format(num))
