import os
import exifread
from decimal import Decimal
from position_utils import *
import requests
import json
import datetime

#  pip3 install exifread

class Location(object):

    def __init__(self, image_path):
        self.img_path = image_path

        self.api_key = "4e8d619c69859ce0f8962de9297c3764" #申请的高德APP web KEY
        #self.api_key = "4f458eaded9bad93b63b8a2c67f5c0e0" #申请的高德APP web KEY
        self.url_get_position = 'https://restapi.amap.com/v3/geocode/regeo?key={}&location={}'

    def run(self):
        # coordinate = self.__get_image_ability()
        coordinate = "116.43213, 38.76623"
        print(f'获取到经度、纬度是:{coordinate}')

        if not coordinate:
            return

        # 根据经度和纬度，获取到详细地址
        address = self.__get_address(coordinate)

        # 检验坐标值
        # https://lbs.amap.com/console/show/picker
        print(f'他当前位置在:{address}')

    def __get_address(self, location):
        """
        根据坐标得到详细地址
        :param location: 经纬度值
        :return:
        """
        resp = requests.get(self.url_get_position.format(self.api_key, location))

        print(resp, resp.json())
        location_data = json.loads(resp.text)

        address = location_data.get('regeocode').get('formatted_address')

        return address

    def __format_lati_long_data(self, data):
        """
        对经度和纬度数据做处理，保留6位小数
        :param data: 原始经度和纬度值
        :return:
        """
        # 删除左右括号和空格
        data_list_tmp = str(data).replace('[', '').replace(']', '').split(',')
        data_list = [data.strip() for data in data_list_tmp]

        # 替换秒的值
        data_tmp = data_list[-1].split('/')

        # 秒的值
        data_sec = int(data_tmp[0]) / int(data_tmp[1]) / 3600

        # 替换分的值
        data_tmp = data_list[-2]

        # 分的值
        data_minute = int(data_tmp) / 60

        # 度的值
        data_degree = int(data_list[0])

        # 由于高德API只能识别到小数点后的6位
        # 需要转换为浮点数，并保留为6位小数
        result = "%.6f" % (data_degree + data_minute + data_sec)
        return float(result)

    def __get_image_ability(self):
        """
        获取图片的属性值，包含：经纬度、拍摄时间等
        :param picture_name:
        :return:
        """

        # 利用exifread库，读取图片的属性
        img_exif = exifread.process_file(open(self.img_path, 'rb'))

        # 能够读取到属性
        if img_exif:
            print(img_exif)
            # 纬度数
            # latitude_gps = img_exif['GPS GPSLatitude']
            latitude_gps = "3540288"
            # N,S 南北纬方向
            # latitude_direction = img_exif['GPS GPSLatitudeRef']

            # 经度数
            # longitude_gps = img_exif['GPS GPSLongitude']
            longgitude_gps = "13421776"
            # E,W 东西经方向
            longitude_direction = img_exif['GPS GPSLongitudeRef']

            # 拍摄时间
            take_time = img_exif['EXIF DateTimeOriginal']

            is_lie = self.judge_time_met(take_time)

            if is_lie:
                print('很遗憾的通知你，他/她在撒谎！！！照片不是今天拍的')
                return

                # 纬度、经度、拍摄时间
            if latitude_gps and longitude_gps and take_time:

                # 对纬度、经度值原始值作进一步的处理
                latitude = self.__format_lati_long_data(latitude_gps)
                longitude = self.__format_lati_long_data(longitude_gps)

                # print(f'{longitude},{latitude}')

                # 注意：由于gps获取的坐标在国内高德等主流地图上逆编码不够精确，这里需要转换为火星坐标系
                location = wgs84togcj02(longitude, latitude)

                return f'{location[0]},{location[1]}'
            else:
                print(f'获取的图片数据属性不完整')
                return ''
        else:
            print('抱歉，图片不是原图，没法获取到图片属性。')
            return ''

    def judge_time_met(self, take_time):
        """
        通知拍摄时间判断女朋友是否撒谎
        :param take_time:
        :return:
        """
        # 拍摄时间
        format_time = str(take_time).split(" ")[0].replace(":", "-")
        print('照片拍摄日期是:')
        print(format_time)
        # 当天日期   验证照片是否是当日拍摄
#        today = str(datetime.date.today())

#        if format_time == today:
#            return False
#        else:
#            return True

if __name__ == '__main__':
    # 女朋友发过来的图片【原图】    #图片命名容易冲突,更换开头就可以
    location = Location('./20221024-151411.jpg')

    # 找到女朋友的地理位置
    location.run()