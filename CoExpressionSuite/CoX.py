

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


def measure_coex(file, size_filter_1, size_filter_2):
    """given a png file and size filters, returns the number of cells
    counted in each channel, as well as the cells counted in both channels"""

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



    return nb_labels_red, nb_labels_green, nb_labels_overlap

def make_coex_image(file, size_filter_1, size_filter_2):
    """given a png file and size filters, returns the number of cells
    counted in each channel, as well as the cells counted in both channels"""

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

    file_name = str(file[:-4])+".coex.png"
    #dir_name = '/'.join(file.split("/")[:-1]) + "/output/coex" + file.split("/")[-1]

    plt.imsave(file_name, cleaned_overlap, cmap='gray')
    print('generating '+ file_name + " from " + file)


def percent_filter(file, size_filter_1, size_filter_2):
    """given a png file and size filters, returns the percent of cells
    counted in each channel that are counted in both"""
    nb_labels_red, nb_labels_green, nb_labels_overlap = measure_coex(file, size_filter_1, size_filter_2)
    percent_of_red = (nb_labels_overlap) / (nb_labels_red)
    percent_of_green  = (nb_labels_overlap) / (nb_labels_green)

    return(file, str(percent_of_red) + " percent red", str(percent_of_green) + " percent green")
