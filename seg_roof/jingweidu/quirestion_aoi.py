import requests
import json
from requests.adapters import HTTPAdapter
from Get_POI_d import Calibration_Tool

def locatebyLatLng(lat, lng, ak, pois=0):
 '''
 根据经纬度查询地址
 '''
 url = "https://api.map.baidu.com/reverse_geocoding/v3/?ak={}&output=json&location={},{}&radius=500&poi_types=工厂|建筑|酒店|公司|大厦|厂房|商场|花园&extensions_poi=1".format(ak, lat, lng)

 # url = "https://api.map.baidu.com/reverse_geocoding/v3/?ak={}&output=json&location={},{}&radius=500&poi_types=工厂|建筑|公司|大厦|厂房&extensions_poi=1&coordtype=wgs84ll".format(ak, lat, lng)

 #url = "https://api.map.baidu.com/reverse_geocoding/v3/?ak={}&output=json&coordtype=bd09ll &location=33.35194364323275, 117.39403228762 &extensions_poi=1".format(ak)
 #  url = "https://api.map.baidu.com/reverse_geocoding/v3/?ak={}&output=json&coordtype=wgs84ll&location={},{}&coordtype=wgs84ll&poi_types=道路|公司".format(ak, lat, lng)

 res = requests.get(url)
 print(res)
 result = res.json()
 print(result)
 print('--------------------------------------------')
 result0 = result['result']['formatted_address'] + ',' + result['result']['sematic_description']
 result1 = result['result']['pois']
 result2 = result['result']['poiRegions'][0]['name']
 print(result2)
 print(result0)
 print(result1)
 return result


def locatebyname(name, city, ak):
 url = "https://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak={}&callback=showLocation".format(name, ak)
 #url = "https://api.map.baidu.com/place/v2/search?query={}&tag=工厂&region={}&output=json&ak={}".format(name, city, ak)

 s = requests.Session()
 s.mount('http://', HTTPAdapter(max_retries=5))
 s.mount('https://', HTTPAdapter(max_retries=5))
 data = s.get(url, timeout=5, headers={"Connection": "close"})  # , proxies=proxies
 print("data:", data)
 data = data.text
 print(data.strip('showLocation&&showLocation('))
 data = data.strip('showLocation&&showLocation(').strip(')')
 data = json.loads(data)
 print(data)
 # res = requests.get(url)
 # result = res.json()
 # print(result)
 # print('--------------------------------------------')
 # result = result['result']['addressComponent']['city']
 # print(result)
 return

def wgs2bd09(lng, lat, ak):
 url = "https://api.map.baidu.com/geoconv/v1/?coords={},{}&from=1&to=5&ak={}".format(lng, lat ,ak)
 res = requests.get(url)
 print(res)
 result = res.json()
 print(result)
 return result



ak = 'QjHcwkGqZfIRHGRu5WvQkA6UPmVsHePz'

# # 广德中威
# 天地图
# lng = 119.48617322
# lat = 30.88915462

# bd09
# lng, lat = 119.497369,30.893669

# wgs84_lat = 30.889287292957306
# wgs84_lng = 119.48536545038223

# 深圳东浩艺术中心
# lng = 114.03677741
# lat = 22.61756991


# 潜龙花园 谷谷GIS上找的
# lng = 114.03716069
# lat = 22.61592014

# 深圳北站 谷谷GIS上找的
# lng = 114.02420468
# lat = 22.61226714

# 深圳北站  百度地图
# lng, lat = 114.037138,22.616667

# 潜龙花园 百度地图上找的坐标
# lng = 114.048748
# lat = 22.619075

# 谷谷GIS上找的， 用转换工具转出来结果不对
# wgs84_lat = 22.61592014
# wgs84_lng = 114.03716069
# tools = Calibration_Tool()
# lng, lat = tools.wgs84_to_bd09(wgs84_lng, wgs84_lat)
# print("lng, lat : ", lng, lat)

# 江西省南昌市青山湖区创新路1号  bd09
# lat = 28.696117043877
# lng = 115.95845796638

# 北京市海淀区中关村大街27号1101-08室   bd09
# lat = 39.983424
# lng = 116.322987

# lat = 38.76623
# lng = 116.43213

# 优奥
# 百度地图
lng, lat = 119.494881,30.897787

# 谷谷GIS
# lng = 119.48299780
# lat = 30.89407509
#
# bd_lng, bd_lat = wgs2bd09(lng, lat, ak)
# exit()

result = locatebyLatLng(lat, lng, ak)
print(result)

# name = "{}".format(result)
name = "公司"
#
# city = "北京市海淀区中关村大街27号1101-08室"
# city = result
city = "深圳北站"
#city = "安徽省宣城市广德市安居路"
locatebyname(name, city, ak)
