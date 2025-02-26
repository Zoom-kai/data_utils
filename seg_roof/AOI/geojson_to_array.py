#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os

os.environ["GDAL_DATA"] = r"/home/pang/anaconda3/envs/zc_ms/share/gdal/"
from osgeo import gdal, osr
import numpy as np
import json
import sys

####################
# download spacenet utilities from:
#  https://github.com/SpaceNetChallenge/utilities/tree/master/python/spaceNet 
path_to_spacenet_utils = '/home/pang/zc/seg/utilities-spacenetV2/python'
sys.path.extend([path_to_spacenet_utils])
from spaceNetUtilities import geoTools as gT


###############################################################################
def geojson_to_pixel_arr(raster_file, geojson_file, pixel_ints=True,  # raster_file ?
                         verbose=False):
    '''
    Tranform geojson file into array of points in pixel (and latlon) coords
    pixel_ints = 1 sets pixel coords as integers
    '''

    # load geojson file
    with open(geojson_file) as f:
        geojson_data = json.load(f)

    # load raster file and get geo transforms
    src_raster = gdal.Open(raster_file)

    # print("src_raster", src_raster)

    targetsr = osr.SpatialReference()
    targetsr.ImportFromWkt(src_raster.GetProjectionRef())

    geom_transform = src_raster.GetGeoTransform()
    #print("geom_transform:{}".format(geom_transform))
    # get latlon coords
    latlons = []
    types = []
    for feature in geojson_data['features']:
        coords_tmp = feature['geometry']['coordinates'][0]
        type_tmp = feature['geometry']['type']
        if verbose:
            print("features:", feature.keys())
            print("geometry:features:", feature['geometry'].keys())

            # print "feature['geometry']['coordinates'][0]", z
        latlons.append(coords_tmp)
        types.append(type_tmp)
        # print feature['geometry']['type']

    # convert latlons to pixel coords
    pixel_coords = []
    latlon_coords = []
    for i, (poly_type, poly0) in enumerate(zip(types, latlons)):

        if poly_type.upper() == 'MULTIPOLYGON':
            # print "oops, multipolygon"
            for poly in poly0:
                poly = np.array(poly)
                if verbose:
                    print("poly.shape:", poly.shape)

                # account for nested arrays
                if len(poly.shape) == 3 and poly.shape[0] == 1:
                    poly = poly[0]

                poly_list_pix = []
                poly_list_latlon = []
                if verbose:
                    print("poly", poly)
                for coord in poly:
                    if verbose:
                        print("coord:", coord)
                    lon, lat, z = coord
                    px, py = gT.latlon2pixel(lat, lon, input_raster=src_raster,
                                             targetsr=targetsr,
                                             geom_transform=geom_transform)
                    poly_list_pix.append([px, py])
                    if verbose:
                        # print("px, py", px, py)
                        print("verbose")
                    poly_list_latlon.append([lat, lon])

                if pixel_ints:
                    ptmp = np.rint(poly_list_pix).astype(int)
                else:
                    ptmp = poly_list_pix
                pixel_coords.append(ptmp)
                latlon_coords.append(poly_list_latlon)

        elif poly_type.upper() == 'POLYGON':
            poly = np.array(poly0)
            if verbose:
                print("poly.shape:", poly.shape)

            # account for nested arrays
            if len(poly.shape) == 3 and poly.shape[0] == 1:
                poly = poly[0]

            poly_list_pix = []
            poly_list_latlon = []
            if verbose:
                print("poly", poly)
            for coord in poly:
                if verbose:
                    print("coord:", coord)
                lon, lat, z = coord
                px, py = gT.latlon2pixel(lat, lon, input_raster=src_raster,
                                         targetsr=targetsr,
                                         geom_transform=geom_transform)
                #print("px, py", px, py)
                poly_list_pix.append([px, py])
                if verbose:
                    print("px, py", px, py)
                poly_list_latlon.append([lat, lon])

            if pixel_ints:
                ptmp = np.rint(poly_list_pix).astype(int)
                #print("pixel_ints !")
            else:
                ptmp = poly_list_pix
            pixel_coords.append(ptmp)
            latlon_coords.append(poly_list_latlon)

        else:
            print("Unknown shape type in coords_arr_from_geojson()")
            return
    return pixel_coords


if __name__ == '__main__':
    print("Running !")
    raster_file = "/home/pang/zc/seg/spacenet/sn2_AOI_4_Shanghai/RGB-PanSharpen/RGB-PanSharpen_AOI_4_Shanghai_img99.tif"
    geojson_file = "/home/pang/zc/seg/spacenet/sn2_AOI_4_Shanghai/geojson/buildings/buildings_AOI_4_Shanghai_img99.geojson"
    print(geojson_to_pixel_arr(raster_file, geojson_file))
