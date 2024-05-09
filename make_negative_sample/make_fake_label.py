import os


img_path = "/mnt/data1/zc_data/green_net_all/green_net/images_fake"
label_path = "/mnt/data1/zc_data/green_net_all/green_net/labels_fake"

if not os.path.exists(label_path):
    os.makedirs(label_path)

img_list = os.listdir(img_path)
for img_name in img_list:
    endwish_name = img_name.split(".")[-1]
    txt_name = img_name.replace(endwish_name, "txt")
    f = open("{}/{}".format(label_path, txt_name), "w")
    f.close()

