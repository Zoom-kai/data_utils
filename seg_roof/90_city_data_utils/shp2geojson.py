
import geopandas as gpd

def Shptogeoj(input_file, output_file):
    data = gpd.read_file(input_file)
    # 指定utf-8编码，防止中文乱码
    data.to_file(output_file, driver="GeoJSON", encoding='utf-8')
    print('Success: File '+input_file.split('\\') [-1] + ' conversion completed')

if __name__ == '__main__':
    # input_file = r"/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier2/Nanjing/Nanjing.shp"
    # output_file = "/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier2/Nanjing/Nanjing.geojson"

    input_file = r"/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/Suzhou.shp"
    output_file = "/mnt/data1/zc_data/map_data/china_90_city_datasets/simplified_Version_1/Tier3/Suzhou/Suzhou.geojson"

    Shptogeoj(input_file,output_file)
