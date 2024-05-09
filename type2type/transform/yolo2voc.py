from xml.dom.minidom import Document
import os
import cv2
import argparse
import random
# def makexml(txtPath, xmlPath, picPath):  # txt所在文件夹路径，xml文件保存路径，图片所在文件夹路径
def makexml(picPath, txtPath, xmlPath, dic):  # txt所在文件夹路径，xml文件保存路径，图片所在文件夹路径
    """此函数用于将yolo格式txt标注文件转换为voc格式xml标注文件
    在自己的标注图片文件夹下建三个子文件夹，分别命名为picture、txt、xml
    """

    files = os.listdir(txtPath)

    if not os.path.exists(xmlPath):
        os.makedirs(xmlPath)
        print("makedirs {} success !".format(xmlPath))
    for i, name in enumerate(files):
        print(name)
        xmlBuilder = Document()
        annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
        xmlBuilder.appendChild(annotation)
        txtFile = open(txtPath + name)
        txtList = txtFile.readlines()
        img = cv2.imread(picPath + name[0:-4] + ".jpeg")
        Pheight, Pwidth, Pdepth = img.shape

        folder = xmlBuilder.createElement("folder")  # folder标签
        foldercontent = xmlBuilder.createTextNode("VOC2007")
        folder.appendChild(foldercontent)
        annotation.appendChild(folder)  # folder标签结束

        filename = xmlBuilder.createElement("filename")  # filename标签
        filenamecontent = xmlBuilder.createTextNode(name[0:-4] + ".jpg")
        filename.appendChild(filenamecontent)
        annotation.appendChild(filename)  # filename标签结束

        # -------------------

        path = xmlBuilder.createElement("path")  # filename标签
        filenamecontent = xmlBuilder.createTextNode("Unknown")
        path.appendChild(filenamecontent)
        annotation.appendChild(path)  # filename标签结束


        source = xmlBuilder.createElement("source")  # filename标签
        database = xmlBuilder.createElement("database")
        filenamecontent = xmlBuilder.createTextNode("The VOC2007 Database")
        database.appendChild(filenamecontent)
        source.appendChild(database)  # filename标签结束
        annotation.appendChild(source)

        size = xmlBuilder.createElement("size")  # size标签
        width = xmlBuilder.createElement("width")  # size子标签width
        widthcontent = xmlBuilder.createTextNode(str(Pwidth))
        width.appendChild(widthcontent)
        size.appendChild(width)  # size子标签width结束

        # ---------------------------
        segmented = xmlBuilder.createElement("segmented")  # segmented
        segmented_0 = xmlBuilder.createTextNode(str(0))
        segmented.appendChild(segmented_0)
        annotation.appendChild(segmented) # size子标签width结束



        height = xmlBuilder.createElement("height")  # size子标签height
        heightcontent = xmlBuilder.createTextNode(str(Pheight))
        height.appendChild(heightcontent)
        size.appendChild(height)  # size子标签height结束

        depth = xmlBuilder.createElement("depth")  # size子标签depth
        depthcontent = xmlBuilder.createTextNode(str(Pdepth))
        depth.appendChild(depthcontent)
        size.appendChild(depth)  # size子标签depth结束

        annotation.appendChild(size)  # size标签结束

        for j in txtList:

            oneline = j.strip().split(" ")
            object = xmlBuilder.createElement("object")  # object 标签
            picname = xmlBuilder.createElement("name")  # name标签
            v = 10 + random.randint(2, 4)*0.1
            print(11111111111111, oneline[0]=="")
            if oneline[0] == "":
                continue
            print(dic)
            print(dic[int(oneline[0])])
            namecontent = xmlBuilder.createTextNode(dic[int(oneline[0])])
            picname.appendChild(namecontent)
            object.appendChild(picname)  # name标签结束

            pose = xmlBuilder.createElement("pose")  # pose标签
            posecontent = xmlBuilder.createTextNode("Unspecified")
            pose.appendChild(posecontent)
            object.appendChild(pose)  # pose标签结束


            # 下面4-7行用来导电压表数据用的
            pose = xmlBuilder.createElement("pose")  # pose标签
            posecontent = xmlBuilder.createTextNode(str(v))
            pose.appendChild(posecontent)
            object.appendChild(pose)  # pose标签结束



            truncated = xmlBuilder.createElement("truncated")  # truncated标签
            truncatedContent = xmlBuilder.createTextNode("0")
            truncated.appendChild(truncatedContent)
            object.appendChild(truncated)  # truncated标签结束

            difficult = xmlBuilder.createElement("difficult")  # difficult标签
            difficultcontent = xmlBuilder.createTextNode("0")
            difficult.appendChild(difficultcontent)
            object.appendChild(difficult)  # difficult标签结束

            bndbox = xmlBuilder.createElement("bndbox")  # bndbox标签
            xmin = xmlBuilder.createElement("xmin")  # xmin标签
            mathData = int(((float(oneline[1])) * Pwidth + 1) - (float(oneline[3])) * 0.5 * Pwidth)
            xminContent = xmlBuilder.createTextNode(str(mathData))
            xmin.appendChild(xminContent)
            bndbox.appendChild(xmin)  # xmin标签结束

            ymin = xmlBuilder.createElement("ymin")  # ymin标签
            mathData = int(((float(oneline[2])) * Pheight + 1) - (float(oneline[4])) * 0.5 * Pheight)
            yminContent = xmlBuilder.createTextNode(str(mathData))
            ymin.appendChild(yminContent)
            bndbox.appendChild(ymin)  # ymin标签结束

            xmax = xmlBuilder.createElement("xmax")  # xmax标签
            mathData = int(((float(oneline[1])) * Pwidth + 1) + (float(oneline[3])) * 0.5 * Pwidth)
            xmaxContent = xmlBuilder.createTextNode(str(mathData))
            xmax.appendChild(xmaxContent)
            bndbox.appendChild(xmax)  # xmax标签结束

            ymax = xmlBuilder.createElement("ymax")  # ymax标签
            mathData = int(((float(oneline[2])) * Pheight + 1) + (float(oneline[4])) * 0.5 * Pheight)
            ymaxContent = xmlBuilder.createTextNode(str(mathData))
            ymax.appendChild(ymaxContent)
            bndbox.appendChild(ymax)  # ymax标签结束

            object.appendChild(bndbox)  # bndbox标签结束

            annotation.appendChild(object)  # object标签结束

        f = open(xmlPath + name[0:-4] + ".xml", 'w')
        # xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t')
        f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', type=str, default=r"/mnt/data1/zzx_data/jx_data/monthtest/05/test_pic/", help='images dir')   # 图片所在文件夹路径，后面的/一定要带上
    parser.add_argument('--xml_path', type=str, default=r"/mnt/data1/zc_code/yolov5-6.0_2/runs/detect/jiangxi_test/labels_xml/", help='xml dir')      # xml文件保存路径，后面的/一定要带上
    parser.add_argument('--txt_path', type=str, default=r"/mnt/data1/zc_code/yolov5-6.0_2/runs/detect/jiangxi_test/labels/", help='txt  dir')  # txt所在文件夹路径，后面的/一定要带上
    parser.add_argument('--classes', type=list, default=
    # ["DLQKG_close", "DLQKG_open"]
    #  ['close', 'open', 'none']
    ['jiangebang', 'wu', 'dengguang', 'shuimian', 'yancong', 'yan']
    # ['HWPTG', 'HWJXG', 'HWJLG', 'HWPBG', 'HWBYG', 'DTUCKG', '400VJXG', '400VLLG', 'GTBQ', 'DYB', 'DDXSQ', 'GTQYJQZT_0',
    #  'GTQYJQZT_1', 'FHKG_0', 'FHKG_1', 'DLQKG_0', 'DLQKG_1', 'GLKG_0', 'GLKG_1', 'DYBHKK_0', 'DYBHKK_1', 'YF/JDCZBS',
    #  'DLQYB', 'DLQYBZSD', 'FHZCZ/ZSMK']

                        , help='classes')  # 类别信息
    args = parser.parse_args()

    img_path = args.img_path
    txt_path = args.txt_path
    xml_path = args.xml_path


    dic = args.classes
    makexml(img_path, txt_path, xml_path, dic)


