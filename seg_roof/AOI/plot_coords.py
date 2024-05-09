#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np


###############################################################################
def plot_truth_coords(input_image, pixel_coords, save_path,
                      figsize=(8, 8), plot_name='test_tif.tif',
                      add_title=False, poly_face_color='orange',
                      poly_edge_color='red', poly_nofill_color='blue', cmap='bwr'):
    '''Plot ground truth coordinaates, pixel_coords should be a numpy array'''

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(2 * figsize[0], figsize[1]))
    print(222)
    if add_title:
        suptitle = fig.suptitle(plot_name.split('/')[-1], fontsize='large')
    input_image = input_image/500
    # create patches
    patches = []
    patches_nofill = []
    print(6666666666666666666, pixel_coords)
    if pixel_coords is not None:
        # get patches
        print(777777777777777, pixel_coords)
        for coord in pixel_coords:
            patches_nofill.append(Polygon(coord, facecolor=poly_nofill_color,
                                          edgecolor=poly_edge_color, lw=3))
            patches.append(Polygon(coord, edgecolor=poly_edge_color, fill=True,
                                   facecolor=poly_face_color))
            print(5555555)
            p0 = PatchCollection(patches, alpha=0.25, match_original=True)
            # p1 = PatchCollection(patches, alpha=0.75, match_original=True)
            p2 = PatchCollection(patches_nofill, alpha=0.75, match_original=True)

    # ax0: raw image
    print(1111)
    ax0.imshow(input_image)
    # if len(patches) > 0:
    #     ax0.add_collection(p0)
    # ax0.set_title('Input Image + Ground Truth Buildings')
    ax0.set_title('Input Image ')
    # truth polygons

    # print("input_image:", input_image)  # input numpy
    zero_arr = np.zeros(input_image.shape[:2])
    # set background to white?
    # zero_arr[zero_arr == 0.0] = np.nan
    ax1.imshow(zero_arr, cmap=cmap)
    if len(patches) > 0:
        ax1.add_collection(p2)
    ax1.set_title('Ground Truth Building Polygons')

    # plt.axis('off')
    plt.tight_layout()
    if add_title:
        suptitle.set_y(0.95)
        fig.subplots_adjust(top=0.96)
    # plt.show()

    if len(plot_name) > 0:
        plt.savefig("{}/{}".format(save_path, plot_name))
    print("Running success !")
    return patches, patches_nofill
