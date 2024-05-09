import requests
from requests.adapters import HTTPAdapter
import json
import math
import re
import numpy as np
import socket
import time

timeout=20

class Baidu_API_tool():             #
    def __init__(self, bmap_key):
        self.bmap_key = bmap_key
        self.calibrate_tool = Calibration_Tool()
    def get_info(self, bmap_localserach_url):
        # bmap_localserach_url = f'http://api.map.baidu.com/place/v2/search?q={POI_category}&region={city}&output=json&ak={self.bmap_key}'
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        data = s.get(bmap_localserach_url, timeout=5, headers={"Connection": "close"})  # , proxies=proxies
        print("data:", data)
        data = data.text
        data = json.loads(data)
        if len(data['results'])>0:
            return data['results']
        else:
            return None

    def getdata(self, url):
        try:
            socket.setdefaulttimeout(timeout)
            html = requests.get(url)
            data = html.json()
            if data['results'] != None:
                return data['results']
            else:
                return None
                # for item in data['results']:
                #     jname = item['name']  # 获取名称
                #     jlat = item['location']['lat']  # 获取经纬度
                #     jlon = item['location']['lng']
                #     jarea = item['area']  # 获取行政区
                #     jadd = item['address']  # 获取具体地址
                #     j_str = jname + ',' + str(jlat) + ',' + str(jlon) + ',' + jarea + ',' + jadd + ',' + '\n'
                #     f.write(j_str)
            # time.sleep(1)
        except:
            getdata(url)


    def POI_boundary(self, uid):
        boundary_request_url = f'https://map.baidu.com/?pcevaname=pc4.1&qt=ext&ext_ver=new&l=12&uid={uid}'
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        data = s.get(boundary_request_url, timeout=5, headers={"Connection": "close"})  # , proxies=proxies
        data = data.text
        data = json.loads(data)
        if 'geo' in data['content'].keys():
            geo_boundary = data['content']['geo'].split('|')[2].split('-')[1].split(',')
        else:
            return None
        # elif 'geo' in data['current_city'].keys():
        #     geo_boundary = data['current_city']['geo'].split('|')[1:]
        #     tmp_str = []
        #     for _ in geo_boundary:
        #         tmp_list = _.split(',')
        #         for tmp_element in tmp_list:
        #             tmp_element = tmp_element.strip(';')
        #             tmp_element = tmp_element.split(';')
        #             tmp_str.extend(tmp_element)
        #     geo_boundary = tmp_str
        i = 0
        coordinates = ''
        for jj in geo_boundary:
            jj = str(jj).strip(';')
            if i % 2 == 0:
                coordinates = coordinates + str(jj) + ','
            else:
                coordinates = coordinates + str(jj) + ';'
            i = i + 1
        coordinates = coordinates.strip(";")
        if len(coordinates.split(';'))<=20:
            corrdinates = self.transform_pingmian_to_coordinates(coordinates)
        else:
            coor_list = coordinates.split(';')
            k_fold = len(coor_list)// 20
            corrdinates = ''
            for coor_i in range(k_fold+1):
                tmp = ';'.join(coor_list[coor_i*20:(coor_i+1)*20])
                corrdinates += self.transform_pingmian_to_coordinates(tmp) + ';'
        # corrdinates = self.transform_pingmian_to_coordinates(coordinates)
        corrdinates = corrdinates.strip(';')
        cor_list = re.split(',|;',corrdinates)
        cor_list = [float(_) for _ in cor_list]
        cor_list = np.array(cor_list).reshape(-1,2)
        cor_lng = cor_list[:,0]
        cor_lat = cor_list[:,1]
        carlib_cor_lng, carlib_cor_lat = self.calibrate_tool.bd09_to_wgs84(cor_lng, cor_lat)
        carlib_zeros = np.zeros_like(carlib_cor_lng).reshape(-1,1)
        cor_list = np.concatenate([carlib_cor_lng.reshape(-1,1), carlib_cor_lat.reshape(-1,1), carlib_zeros],axis=1)
        i = 0
        coordinates = ''
        for jj in cor_list.reshape(-1):
            jj = str(jj).strip(';')
            if i % 3 == 0 or i % 3 == 1:
                coordinates = coordinates + str(jj) + ','
            else:
                coordinates = coordinates + str(jj) + ';'
            i = i + 1
        coordinates = coordinates.replace(';', ' ')
        return coordinates

    def transform_pingmian_to_coordinates(self, coordinates):   # ??
        req_url = 'http://api.map.baidu.com/geoconv/v1/?coords=' + coordinates + '&from=6&to=5&ak=' + self.bmap_key
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        data = s.get(req_url, timeout=5, headers={"Connection": "close"})  # , proxies=proxies
        data = data.text
        data = json.loads(data)
        coords = ''
        if data['status'] == 0:
            try:
                result = data['result']
                if len(result) > 0:
                    for res in result:
                        lng = res['x']
                        lat = res['y']
                        coords = coords + ";" + str(lng) + "," + str(lat)
                return coords.strip(";")
            except Exception as e:
                print(f'Error\t{req_url}')
                return None
        else:
            return None



class Calibration_Tool:       # 校准工具
    def __init__(self):
        self.x_pi = 3.14159265358979324 * 3000.0 / 180.0    # ？？
        self.pi = 3.1415926535897932384626  # π
        self.a = 6378245.0  # 长半轴
        self.ee = 0.00669342162296594323  # 偏心率平方

    def gcj02_to_bd09(self, lng, lat):
        """
        火星坐标系(GCJ-02)转百度坐标系(BD-09)
        谷歌、高德——>百度
        :param lng:火星坐标经度
        :param lat:火星坐标纬度
        :return:
        """
        z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * self.x_pi)
        theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * self.x_pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return [bd_lng, bd_lat]

    def bd09_to_gcj02(self, bd_lon, bd_lat):
        """
        百度坐标系(BD-09)转火星坐标系(GCJ-02)
        百度——>谷歌、高德
        :param bd_lat:百度坐标纬度
        :param bd_lon:百度坐标经度
        :return:转换后的坐标列表形式
        """
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = np.sqrt(x * x + y * y) - 0.00002 * np.sin(y * self.x_pi)
        theta = np.arctan2(y, x) - 0.000003 * np.cos(x * self.x_pi)
        gg_lng = z * np.cos(theta)
        gg_lat = z * np.sin(theta)
        return [gg_lng, gg_lat]

    def wgs84_to_gcj02(self, lng, lat):
        """
        WGS84转GCJ02(火星坐标系)
        :param lng:WGS84坐标系的经度
        :param lat:WGS84坐标系的纬度
        :return:
        """
        if self.out_of_china(lng, lat).any():  # 判断是否在国内
            return [lng, lat]
        dlat = self._transformlat(lng - 105.0, lat - 35.0)
        dlng = self._transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = np.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = np.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * np.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [mglng, mglat]

    def gcj02_to_wgs84(self, lng, lat):
        """
        GCJ02(火星坐标系)转GPS84
        :param lng:火星坐标系的经度
        :param lat:火星坐标系纬度
        :return:
        """
        if self.out_of_china(lng, lat).any():
            return [lng, lat]
        dlat = self._transformlat(lng - 105.0, lat - 35.0)
        dlng = self._transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = np.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = np.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * np.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [lng * 2 - mglng, lat * 2 - mglat]

    def bd09_to_wgs84(self, bd_lon, bd_lat):
        lon, lat = self.bd09_to_gcj02(bd_lon, bd_lat)
        return self.gcj02_to_wgs84(lon, lat)

    def wgs84_to_bd09(self, lon, lat):
        lon, lat = self.wgs84_to_gcj02(lon, lat)
        return self.gcj02_to_bd09(lon, lat)

    def _transformlat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
              0.1 * lng * lat + 0.2 * np.sqrt(np.fabs(lng))
        ret += (20.0 * np.sin(6.0 * lng * self.pi) + 20.0 *
                np.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * np.sin(lat * self.pi) + 40.0 *
                np.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * np.sin(lat / 12.0 * self.pi) + 320 *
                np.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    def _transformlng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
              0.1 * lng * lat + 0.1 * np.sqrt(np.fabs(lng))
        ret += (20.0 * np.sin(6.0 * lng * self.pi) + 20.0 *
                np.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * np.sin(lng * self.pi) + 40.0 *
                np.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * np.sin(lng / 12.0 * self.pi) + 300.0 *
                np.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    def out_of_china(self, lng, lat):
        """
        判断是否在国内，不在国内不做偏移
        :param lng:
        :param lat:
        :return:
        """
        return ~((lng > 73.66) & (lng < 135.05) & (lat > 3.86) & (lat < 53.55))


def method_region(tag,city_name):
    urls=[] #声明一个数组列表
    for i in range(0,20):
        page_num=str(i)
        url='http://api.map.baidu.com/place/v2/search?query='+tag+'&region='+city_name+'&page_size=20&page_num='+str(page_num)+'&output=json&ak='+ak
        urls.append(url)

def getdata(url):
    try:
        socket.setdefaulttimeout(timeout)
        html=requests.get(url)
        data=html.json()
        if data['results']!=None:
            for item in data['results']:
                    jname=item['name']#获取名称
                    jlat=item['location']['lat']#获取经纬度
                    jlon=item['location']['lng']
                    jarea=item['area']#获取行政区
                    jadd=item['address']#获取具体地址
                    j_str=jname+','+str(jlat)+','+str(jlon)+','+jarea+','+jadd+','+'\n'
                    f.write(j_str)
        #time.sleep(1)
    except:
        getdata(url)


def method_bounds(lng_r, lng_l, lat_r, lat_l):

    lng_c=lng_r-lng_l
    lat_c=lat_r-lat_l

    lng_num=int(lng_c/0.1)+1#以0.1度划分区域
    lat_num=int(lat_c/0.1)+1

    arr=np.zeros((lat_num+1,lng_num+1,2))#组成新的经纬度区域
    for lat in range(0,lat_num+1):
        for lng in range(0,lng_num+1):
            arr[lat][lng]=[lng_l+lng*0.1,lat_l+lat*0.1]

    urls=[]
    for lat in range(0,lat_num):
        for lng in range(0,lng_num):
            for b in range(0,20):
                page_num=str(b)
                url='http://api.map.baidu.com/place/v2/search?query='+POI_category+'&bounds='+str((arr[lat][lng][0]))+','+str((arr[lat][lng][1]))+','+str((arr[lat+1][lng+1][0]))+','+str((arr[lat+1][lng+1][1]))+'&page_size=20&page_num='+str(page_num)+'&output=json&ak='+map_key
                # print(url)
                urls.append(url)
    print('url列表读取完成')
    return urls
    # for url in urls:
    #     getdata(url)
    #     print('爬取中，请耐心等待')
    # f.close()
    # print('完成，文件位于D盘目录下，请查看')


if __name__ == '__main__':
    POI_category = '小区'
    city = '北京'
    map_key = 'xfyTTOTcrGsUroFi7NhoXP6oQ5I61j1v'

    POI_tool = Baidu_API_tool(map_key)
    Calib_Tool = Calibration_Tool()

    f = open(r'D:\POI-' + POI_category + '.txt', 'a', encoding='utf-8')  # 存储文件
    #((lng > 73.66) & (lng < 135.05) & (lat > 3.86) & (lat < 53.55))
    url_list = method_bounds(100, 80, 53, 46)
    
    for url in url_list:
        POIs = POI_tool.getdata(url)
        print(POIs)
        for POI in POIs:
            name = POI['name']
            # lng是经度（东、西）， lat是纬度（南、北）
            lng, lat = POI['location']['lng'], POI['location']['lat']
            POI['location'] = Calib_Tool.bd09_to_wgs84(lng, lat)
            POI_uid = POI['uid']
            boundary = POI_tool.POI_boundary(POI_uid)
            print(name, ' location: ', POI['location'])
            print(boundary)

