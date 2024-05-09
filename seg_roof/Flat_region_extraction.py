import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import segmentation
from skimage.future import graph


class FlatRegionExtraction():
    def __init__(self,
                 region_area_thresh = 100,
                 resolution = 0.6,
                 shorter_length_thresh = 10,
                 empty_ratio = 0.6):
        self.region_area_thresh = region_area_thresh
        self.resolution = resolution
        self.shorter_length_thresh = shorter_length_thresh
        self.empty_ratio = empty_ratio
        self.region_area_thresh_pixel = self.region_area_thresh / (self.resolution**2)
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

    def _weight_mean_color(self,graph, src, dst, n):
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

    def select_solar_regions(self,labels):
        ind_max = labels.max() + 1
        results = 0
        for ind in range(ind_max):
            results += self.is_suitable_for_solar(labels,
                                                     ind,
                                                     area_thresh= self.region_area_thresh_pixel,
                                                     shorter_length_thresh= self.shorter_length_thresh_pixel,
                                                     empty_ratio=self.empty_ratio)
        return results

    def __call__(self, img, ):

        # use traditional segmentation to extract flat regions
        labels = segmentation.slic(img, compactness=40, n_segments=400, start_label=1)
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



if __name__ == '__main__':
    img_path = 'images/building.png'
    img = cv2.imread(img_path)
    extractor = FlatRegionExtraction(region_area_thresh = 100,
                         resolution = 0.6,
                         shorter_length_thresh = 10,
                         empty_ratio = 0.6)
    flat_regions = extractor(img)
    plt.imsave('result.png',flat_regions)