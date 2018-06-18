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


glob_dir = input("Enter Directory ")
glob_File_type = input("Enter File Extension ")

#input_request = input("enter file name")
size_filter_1 = input("size_filter 1: ")
size_filter_2 = input("size_filer 2: ")
output_file = input("output file: ")
#def filter(input_request, size_filter_1, size_filter_2):
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

    #for cleaned overlap, not sure what value to set:
    cleaned_overlap = morphology.remove_small_objects(overlap, min(int(size_filter_1),int(size_filter_2)))

    label_im_overlap, nb_labels_overlap = ndimage.label(cleaned_overlap, structure=None)
    print("----------")
    print(file)
    print(nb_labels_red, ' red cells')

    print(nb_labels_green, ' green cells')

    print(nb_labels_overlap, 'overlapping cells')

    vals = str([file, nb_labels_red, nb_labels_green, nb_labels_overlap])
    output = vals
    fd = open(output_file + '.csv','a')
    fd.write(output)
    fd.close()

#filter(file, size_filter_1, size_filter_2)

glob_files = glob.glob(glob_dir + '/*' + glob_File_type)
for file in glob_files:
    filter(file, size_filter_1, size_filter_2)
    continue
