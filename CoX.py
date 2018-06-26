

import cv2
from skimage import color
from skimage import io
from skimage import data
from skimage.feature import canny
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from scipy import ndimage as ndi
import glob
from skimage import morphology
import matplotlib
from PIL import Image
import scipy.misc


def filter(file, size_filter_1, size_filter_2):


    png_file = io.imread(file)
    channel1, channel2 = [png_file[:,:,0], png_file[:,:,1]]

    edges_red = canny(channel1)
    edges_green = canny(channel2)

    fill_cells_red = ndi.binary_fill_holes(edges_red)
    fill_cells_green = ndi.binary_fill_holes(edges_green)

    cells_cleaned_red = morphology.remove_small_objects(fill_cells_red, int(size_filter_1))
    cells_cleaned_green = morphology.remove_small_objects(fill_cells_green, int(size_filter_2))

    label_im_red, nb_labels_red = ndimage.label(cells_cleaned_red, structure=None)
    label_im_green, nb_labels_green = ndimage.label(cells_cleaned_green, structure=None)

    overlap = np.array(cells_cleaned_green & cells_cleaned_red)
    cleaned_overlap = morphology.remove_small_objects(overlap, min(int(size_filter_1),int(size_filter_2)))
    label_im_overlap, nb_labels_overlap = ndimage.label(cleaned_overlap, structure=None)

    return (nb_labels_red, nb_labels_green, nb_labels_overlap)
