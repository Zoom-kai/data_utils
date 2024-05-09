import matplotlib.pyplot as plt
import numpy as np
import cv2
from tqdm import tqdm
from matplotlib import cm
import pickle as pkl
import torch
import os
from skimage import segmentation
from skimage.future import graph

class FlatRegionExtraction():
    def __init__(self,
                 region_area_thresh=100,
                 resolution=0.6,
                 shorter_length_thresh=10,
                 empty_ratio=0.6):
        self.region_area_thresh = region_area_thresh
        self.resolution = resolution
        self.shorter_length_thresh = shorter_length_thresh
        self.empty_ratio = empty_ratio
        self.region_area_thresh_pixel = self.region_area_thresh / (self.resolution ** 2)
        self.shorter_length_thresh_pixel = self.shorter_length_thresh / self.resolution

    def merge_mean_color(self, graph, src, dst):
        """Callback called before merging two nodes of a mean color distance graph.

        This method computes the mean color of `dst`.

        Parameters
        ----------
        graph : RAG
            The graph under consideration.
        src, dst : int
            The vertices in `graph` to be merged.
        """
        graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
        graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
        graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                          graph.nodes[dst]['pixel count'])

    def _weight_mean_color(self, graph, src, dst, n):
        """Callback to handle merging nodes by recomputing mean color.

        The method expects that the mean color of `dst` is already computed.

        Parameters
        ----------
        graph : RAG
            The graph under consideration.
        src, dst : int
            The vertices in `graph` to be merged.
        n : int
            A neighbor of `src` or `dst` or both.

        Returns
        -------
        data : dict
            A dictionary with the `"weight"` attribute set as the absolute
            difference of the mean color between node `dst` and `n`.
        """

        diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
        diff = np.linalg.norm(diff)
        return {'weight': diff}

    def select_solar_regions(self, labels):
        ind_max = labels.max() + 1
        results = 0
        for ind in range(ind_max):
            results += self.is_suitable_for_solar(labels,
                                                  ind,
                                                  area_thresh=self.region_area_thresh_pixel,
                                                  shorter_length_thresh=self.shorter_length_thresh_pixel,
                                                  empty_ratio=self.empty_ratio)
        return results

    def __call__(self, img, ):

        # use traditional segmentation to extract flat regions
        # labels = segmentation.slic(img, compactness=40, n_segments=400, start_label=1)
        print(888888888888888888888, img)
        labels = segmentation.slic(img, compactness=40, n_segments=400)
        g = graph.rag_mean_color(img, labels)
        labels = graph.merge_hierarchical(labels, g, thresh=40, rag_copy=False,
                                          in_place_merge=True,
                                          merge_func=self.merge_mean_color,
                                          weight_func=self._weight_mean_color)
        labels = self.select_solar_regions(labels)
        # post process
        labels_final = self.post_process(img, labels)
        return labels_final

    def post_process(self, img, labels):
        mask = img.mean(axis=-1) != 0
        labels_final = labels * mask
        return labels_final

    def is_suitable_for_solar(self,
                              labels,
                              ind,
                              area_thresh=100,
                              empty_ratio=0.3,
                              shorter_length_thresh=10):

        region_i = labels == ind
        region_i_processed = region_i.astype(np.uint8) * 255
        zero_img = np.zeros_like(region_i_processed)
        region_area = region_i.sum()
        if region_area <= area_thresh:
            return zero_img

        contours, hierarchy = cv2.findContours(region_i_processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        is_pass = 0
        for c in contours:
            box = cv2.minAreaRect(c)
            height = box[1][0]
            width = box[1][1]
            box_area = height * width
            ##### for debug #######
            # a = np.zeros([labels.shape[0], labels.shape[1],3]).astype(np.uint8)
            # box = cv2.boxPoints(box)
            # box = np.int0(box)
            # a = cv2.drawContours(a, [box], 0, (0, 0, 255), 3)
            # plt.imsave('111.png',a)
            ########################
            if (height < shorter_length_thresh) | (width < shorter_length_thresh):
                continue
            if (1 - region_area / box_area) >= empty_ratio:
                continue
            is_pass = 1
        if is_pass == 1:
            return region_i
        else:
            return zero_img

def extract_roof_from_output_mask(mask, resolution = 0.59,
                 area_thresh = 1500,
                 height_thresh = 40,
                 width_thresh = 40,
                 use_cuda = True, gpu_id='1'):

    _, instances = cv2.connectedComponents(mask)
    locations = []

    if use_cuda:
        instances = torch.from_numpy(instances).to('cuda:{}'.format(gpu_id))
        for instance_i_num in range(1, instances.max()):
            index = instances == instance_i_num
            index_center_x, index_center_y = torch.where(index)
            index_x_min = index_center_x.min()
            index_x_max = index_center_x.max()
            index_y_min = index_center_y.min()
            index_y_max = index_center_y.max()
            local_index = index[index_x_min:index_x_max, index_y_min:index_y_max]
            height = index_center_x.max() - index_center_x.min()
            width = index_center_y.max() - index_center_y.min()

            if width < width_thresh or height < height_thresh:
                # instances[index] = 0
                # dst[index] = 0
                continue
            area = index.sum() * (resolution ** 2)
            if area < area_thresh:
                # instances[index] = 0
                # dst[index] = 0
                continue
            locations.append(
                [index_x_min.cpu().numpy(), index_x_max.cpu().numpy(), index_y_min.cpu().numpy(), index_y_max.cpu().numpy(),
                 local_index.cpu().numpy()])

    else:
        for instance_i_num in range(1, instances.max()):
            index = instances == instance_i_num
            index_center_x, index_center_y = np.where(index)
            index_x_min = index_center_x.min()
            index_x_max = index_center_x.max()
            index_y_min = index_center_y.min()
            index_y_max = index_center_y.max()
            local_index = index[index_x_min:index_x_max, index_y_min:index_y_max]
            height = index_center_x.max() - index_center_x.min()
            width = index_center_y.max() - index_center_y.min()

            if width < width_thresh or height < height_thresh:
                instances[index] = 0
                mask[index] = 0
                continue
            area = index.sum() * (resolution ** 2)
            if area < area_thresh:
                instances[index] = 0
                mask[index] = 0
                continue
            locations.append([index_x_min, index_x_max, index_y_min, index_y_max, local_index])

    return locations

def crop_roof_from_satellite_image(img_path, locations, save_path, extractor, mask):
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    print(3333333333333333333)
    i = 0
    print(locations)

    img = cv2.imread(img_path)
    img2 = img.copy()
    mask_list = []
    for location_i in locations:
        background1 = np.zeros((img.shape[0], img.shape[1]))

        # plt.imshow(location_i[4])
        # plt.show()
        # plt.close()

        # plt.imshow(img)
        # plt.show()
        # plt.close()
        # img = cv2.imread(img_path)
        roof = img[location_i[0]:location_i[1],location_i[2]:location_i[3]].copy()

        # plt.imshow(roof)
        # plt.show()
        # plt.close()
        roof[location_i[4]==False] = 0.0

        # plt.imshow(roof)
        # plt.show()

        pingzhen_roof = extractor(roof)

        print(pingzhen_roof[pingzhen_roof!=0])
        # plt.imshow(pingzhen_roof)
        # plt.show()

        # exit()
        print(pingzhen_roof[pingzhen_roof!=0])
        pingzhen_roof[pingzhen_roof==1] = 255
        # pingzhen_roof[pingzhen_roof == 1] = 0

        # mask1 = mask[location_i[0]:location_i[1],location_i[2]:location_i[3]]
        # plt.imshow(mask1)
        # plt.show()

        background1[location_i[0]:location_i[1],location_i[2]:location_i[3]] =  pingzhen_roof

        mask_list.append(background1)
        # plt.imshow(background)
        # plt.show()
        # exit()
        # print(111111111111111111111)

        i +=1
    return mask_list

if __name__ == "__main__":

    img_path = r"/mnt/data1/zc_data/map_data/tianditu_merge/test/ningbo/ningbo_ori/"
    mask_path = r"/mnt/data1/zc_data/map_data/tianditu_merge/test/ningbo/ningbo_jiedaotu_masks/"
    save_path = "ningbo/output_roof"

    img_list = os.listdir(img_path)
    mask_list = os.listdir(mask_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for name in img_list:

        mask = cv2.imread("{}/{}".format(mask_path, name), cv2.IMREAD_GRAYSCALE)
        mask[mask==1] = 255
        img_path = "{}/{}".format(img_path, name)
        img = cv2.imread(img_path)

        print(mask, mask.shape)

        locations = extract_roof_from_output_mask(mask)

        print(locations)

        extractor = FlatRegionExtraction(region_area_thresh=100,
                                         resolution=0.6,
                                         shorter_length_thresh=10,
                                         empty_ratio=0.6)

        mask_list = crop_roof_from_satellite_image(img_path, locations, save_path, extractor, mask)

        new_mask = 0
        for patch in mask_list:
            new_mask += patch
            # plt.imshow(patch)
            # plt.show()
        new_mask[new_mask != 0] = 255
        plt.imshow(new_mask)
        plt.show()
        cv2.imwrite(os.path.join(save_path, name), new_mask)